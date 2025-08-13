import json
import requests
import traceback
import boto3
import time
from paramiko import SSHClient
import paramiko
from time import sleep
from util_functions import *
from ollama_api_methods import *
from boto_commands import params

resource = boto3.resource('ec2', region_name = 'eu-north-1')
client = boto3.client('ec2', region_name = 'eu-north-1')
instance_id = ''
security_group_id = ''
resource = boto3.resource('ec2', region_name = 'eu-north-1')
client = boto3.client('ec2', region_name = 'eu-north-1')
try:
	
	#configs - make these be taken through cmd line
	
	instance_type = "g6.xlarge"
	
	ami_id = "ami-0c46fc11370489f11"
	
	key_name = "john key"
	
	
	
	unique_name = str(time.time())
	
	local_ip = get_local_ip()
	
	print(local_ip)
	security_group_list = get_security_groups_with_inbound_rule(local_ip, client)
	print(security_group_list)
	
	if len(security_group_list) == 0:
		vpc_id = get_vpc_id(client)
		security_group_id = create_and_configure_security_group(unique_name, vpc_id, local_ip, client)
	else:
		security_group_id = security_group_list[0]['GroupId']		
	
	
	
	params['TagSpecifications'][0]['Tags'][0]['Value'] = unique_name
	params['NetworkInterfaces'][0]['Groups'] = [security_group_id]
	params['InstanceType'] = instance_type
	params['KeyName'] = key_name
	params['ImageId'] = ami_id
	
	
	#print(params)	
	
	instance = resource.create_instances(**params)
	
	instance = instance[0]
	
	instance.wait_until_running()
	
	instance.load()
	
	instance_id = instance.id
	
	public_dns_name = instance.public_dns_name
	
	print("use this for openwebui")
	
	print(public_dns_name)
	
	sleep(10)
	
	#waiter = client.get_waiter('instance_status_ok')
	
	sshclient = SSHClient()
	
	sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	
	print("attempting to form ssh connection")
	
	key_filename = key_name + ".pem"
	
	sshclient.connect(public_dns_name, username = 'ubuntu', key_filename = key_filename)
	
	print('starting install command')
	
	
	run_cmd("curl -fsSL https://ollama.com/install.sh | sh", sshclient)

	# Stop systemd service and disable auto-start
	run_cmd("sudo systemctl stop ollama", sshclient)
	run_cmd("sudo systemctl disable ollama", sshclient)

	# Kill any lingering processes
	run_cmd("pkill -f 'ollama'", sshclient)

	# Start Ollama on 0.0.0.0:11434
	# NOTE: use a separate shell to launch it in background without PTY issues
	run_cmd("nohup bash -c 'OLLAMA_HOST=0.0.0.0:11434 ollama serve > ollama.log 2>&1  &'", sshclient)

	# Wait a few seconds to let server start
	sleep(5)

	# Check if Ollama is running from inside EC2 (localhost works, not 0.0.0.0)
	run_cmd("curl -s http://localhost:11434 || echo 'Ollama not listening'", sshclient)	
	
	base_url = 'http://' + public_dns_name + ":11434" 
	
	print("pulling model")
	
	
	model_pull = {"name": model_name, "stream": False}
	
	pull_response = pull_model(model_pull, base_url)
	print("you can use this api endpoint if you want")
	print(base_url)
	
	print(pull_response)
	
	input("type anything to close the container")
	
	print(client.terminate_instances(InstanceIds=[instance_id]))
	
	
	
except Exception as e: #terminating container when done
	print(traceback.format_exc())
	print(client.terminate_instances(InstanceIds=[instance_id]))
	


