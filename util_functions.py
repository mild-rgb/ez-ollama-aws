import json
import os
import requests
import boto3
from requests import get
import time
import shlex


class JsonHandler:
    def __init__(self, filename):
        self.filename = filename
        self.data = self._load_data()

    def _load_data(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
            except FileNotFoundError:
                with open(self.filename, "w") as f:
                    json.dump({}, f)
        return {}

    def _save_data(self):
        with open(self.filename, "w") as f:
            json.dump(self.data, f)

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self._save_data() 


#turn all of these into a class


class AWSNetworkManager:
    def __init__(self, client):
        self.client = client

    def _get_security_groups_with_inbound_rule(self, local_ip, client):
        security_groups = []
        next_token = None
        while True:
            params = {
                'Filters': [
                    {
                        'Name': 'ip-permission.cidr',
                        'Values': [local_ip]
                    }
                ],
                'MaxResults': 1000  # maximum number of results per request
            }
            if next_token:
                params['NextToken'] = next_token  # loop through describe_security_groups

            response = self.client.describe_security_groups(**params)
            print(response)
            security_groups.extend(response['SecurityGroups'])

            next_token = response.get('NextToken')
            if not next_token:
                break

        return security_groups

    def _create_and_configure_security_group(self, unique_name, vpc_id, local_ip, client):

        # Create the security group with a description and a friendly name
        response = self.client.create_security_group(
            Description='Security group allowing SSH and custom TCP traffic',
            GroupName=unique_name,
            VpcId=vpc_id
        )

        # Extract the security group ID from the response
        security_group_id = response['GroupId']
        print(f"Security Group Created {security_group_id} in VPC {vpc_id}")

        # defining the inbound rules to allow ssh on port 22 and custom TCP on port 8080
        ip_permissions = [
            {
                'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{'CidrIp': local_ip}]
            },
            {
                'IpProtocol': 'tcp',
                'FromPort': 8080,
                'ToPort': 8080,
                'IpRanges': [{'CidrIp': local_ip}]
            }
        ]

        # Authorize the inbound rules on the security group
        client.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=ip_permissions
        )
        print("Inbound rules for SSH and custom TCP added.")

        return security_group_id

    def _get_local_ip(self):
        try:
            ip = str(get('https://checkip.amazonaws.com').text.strip())
            ip = ip + "/32"
            return ip
        except Exception as e:
            print(e)
            print("you're not connected to the internet or aws is down")

    def _get_vpc_id(self, vpc_id=None):  # get a specific vpc object if it's available. if it's not, get the default one
        # If a VPC ID is provided, describe that specific VPC
        if vpc_id:
            response = self.client.describe_vpcs(
                VpcIds=[vpc_id]
            )
        else:
            # Otherwise, get the default VPC by filtering on is-default = true
            response = self.client.describe_vpcs(
                Filters=[{
                    'Name': 'is-default',
                    'Values': ['true']
                }]
            )

        vpcs = response.get('Vpcs', [])

        if not vpcs:
            print("No VPC found.")
            return None

        # Return the VPC ID (or list if you want more details)
        selected_vpc = vpcs[0]  # There should only be one default VPC
        return selected_vpc['VpcId']

    def get_security_group(self, vpc_id=None):
        local_ip = self._get_local_ip()
        security_group_list = self._get_security_groups_with_inbound_rule(local_ip, self.client)
        print(len(security_group_list))
        if len(security_group_list) == 0:
            print("length was 0")
            id = self._get_vpc_id(vpc_id)
            unique_name = str(time.time())
            security_group_id = self._create_and_configure_security_group(unique_name, id, local_ip, self.client)
        else:
            print("length was 1")
            security_group_id = security_group_list[0]['GroupId']
        return security_group_id


def create_ebs_disk(client):
    response = client.create_volume(
        AvailabilityZone='eu-north-1b',
        Size=100,
        VolumeType='gp3',
    )
    diskid = response.get('VolumeId')
    return diskid

class RunCMD:
    def __init__(self, sshclient):
        self.sshclient = sshclient

    def execute(self, cmd):
        return self.__run_cmd(cmd)

    def exec_until_no_error(self, cmd, err_mesg='', retries=5, delay=2): #use - use if any error messages are allowable. in this particular case, format_and_mount returns version in error, even when it passess succesfully
        for attempt in range(retries):
            result = self.__run_cmd(cmd)
            if err_mesg in result:
                return result
            print(f"try {attempt} failed")
            time.sleep(delay)
        raise RuntimeError(f"command failed after {retries} retries: {cmd}")

    def __run_cmd(self, command):
        print(f"Running: {command}")
        stdin, stdout, stderr = self.sshclient.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()
        print("Output:", output)
        print("Error:", error)
        return error    

    def make_exec(self, absolute_path, filename, content):
        self.make_file_and_write_in(absolute_path, filename, content)
        self.__run_cmd('sudo chmod +x ' + absolute_path + filename)
        

    def make_file_and_write_in(self, absolute_path, filename, content=''):
        command = 'cd / && cd ' + absolute_path + ' && sudo touch ' + filename
        self.__run_cmd(command)
        self.__overwrite_text_into_file(content, filename, absolute_path)

    def make_folder(self, absolute_path, name):
        command = 'sudo mkdir ' + absolute_path + '/' + name
        self.__run_cmd(command) 

    def __overwrite_text_into_file(self, text, filename, absolute_path):
        quoted_text = shlex.quote(text)
        command = f"cd / && cd {absolute_path} && echo {quoted_text} | sudo tee {filename} >/dev/null"
        self.__run_cmd(command)

    def overwrite_systemd_file(self, filename, content):
         path_to_systemd = '/etc/systemd/system/'
         self.__overwrite_text_into_file(content, filename, path_to_systemd)
         restart_cmd = 'sudo systemctl daemon-reload && sudo systemctl restart ' + filename
         self.__run_cmd(restart_cmd)
