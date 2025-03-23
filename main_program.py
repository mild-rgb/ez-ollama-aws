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
instance_id = ''
terminal_input = ''
url = ''
user_input = ''
security_group_id = ''
resource = boto3.resource('ec2', region_name = 'eu-north-1')
client = boto3.client('ec2', region_name = 'eu-north-1')
try:
	
	#configs - make these be taken through cmd line
	model_name = "gemma3:12b"
	
	instance_type = "c5.2xlarge"
	
	key_name = 'laptop_key'
	
	
	
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
	
	
	#print(params)	
	
	instance = resource.create_instances(**params)
	
	instance = instance[0]
	
	instance.wait_until_running()
	
	instance.load()
	
	instance_id = instance.id
	
	public_dns_name = instance.public_dns_name
	
	print(public_dns_name)
	
	print(instance_id)
	
	waiter = client.get_waiter('instance_status_ok')
	
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
	
	
	
	
	while True:
		user_input = input("query: ")
		if user_input == 'quit':
			break
		model_data = {"model": model_name, "prompt": user_input, "stream": False}
		response = generate_response(model_data, base_url)
		print(response)
		eval_time = response.get('eval_duration')
		eval_time_seconds = (eval_time/1000000000)
		token_count = response.get('eval_count')
		time_per_token = token_count / eval_time_seconds
		print("time per token: " + str(time_per_token))
		print("eval time: " + str(eval_time_seconds))
		print("token count: " + str(token_count))
		print(response['response'])
	
	
	print(client.terminate_instances(InstanceIds=[instance_id]))
	
	
except KeyboardInterrupt:
	print(client.terminate_instances([instance_id]))
	
except Exception as e: #terminating container when done
	print(traceback.format_exc())
	print(client.terminate_instances(InstanceIds=[instance_id]))
	
	
	'''
	 
 
 groups = get_security_groups_with_inbound_rule(ip)
 print(groups)
 '''
	
