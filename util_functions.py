import json
import requests
import boto3 
from requests import get 


def run_cmd(command, client):
    print(f"Running: {command}")
    stdin, stdout, stderr = client.exec_command(command)
    output = stdout.read().decode()
    error = stderr.read().decode()
    print("Output:", output)
    print("Error:", error)	
    

def get_local_ip():
 try:
 	ip = str(get('https://checkip.amazonaws.com').text.strip())
 	ip = ip + "/32"
 	return ip
 except Exception as e:
 	print(e)
 	print("you're not connected to the internet or aws is down")
 	

def get_vpc_id(vpc_id=None):
    ec2 = boto3.client('ec2')
    
    # If a VPC ID is provided, describe that specific VPC
    if vpc_id:
        response = ec2.describe_vpcs(
            VpcIds=[vpc_id]
        )
    else:
        # Otherwise, get the default VPC by filtering on is-default = true
        response = ec2.describe_vpcs(
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
    
    
def create_and_configure_security_group(unique_name, vpc_id, local_ip):
    # Initialize the EC2 client
    ec2 = boto3.client('ec2')
    
    # Create the security group with a description and a friendly name
    response = ec2.create_security_group(
        Description='Security group allowing SSH and custom TCP traffic',
        GroupName=unique_name,
        VpcId=vpc_id
    )
    
    # Extract the security group ID from the response
    security_group_id = response['GroupId']
    print(f"Security Group Created {security_group_id} in VPC {vpc_id}")
    
    # Define the inbound rules to allow SSH (port 22) and custom TCP (port 11434)
    ip_permissions = [
        {
            'IpProtocol': 'tcp',
            'FromPort': 22,
            'ToPort': 22,
            'IpRanges': [{'CidrIp': local_ip}]
        },
        {
            'IpProtocol': 'tcp',
            'FromPort': 11434,
            'ToPort': 11434,
            'IpRanges': [{'CidrIp': local_ip}]
        }
    ]
    
    # Authorize the inbound rules on the security group
    ec2.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=ip_permissions
    )
    print("Inbound rules for SSH and custom TCP added.")
    
    return security_group_id


def get_security_groups_with_inbound_rule(local_ip):
    ec2 = boto3.client('ec2')
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
            params['NextToken'] = next_token

        response = ec2.describe_security_groups(**params)
        print(response)
        security_groups.extend(response['SecurityGroups'])

        next_token = response.get('NextToken')
        if not next_token:
            break

    return security_groups
    	
