import subprocess
import json
import requests
import traceback
from paramiko import SSHClient
import paramiko
instance_id = ''
terminal_input = ''
url = ''
user_input = ''
from util_functions import *
from ollama_api_methods import *
from time import sleep
try:

	#initiating container 


	result = subprocess.run(['sh containerinit.sh'], shell=True, text=True, capture_output=True)
	
	sleep(1)

	output_dict = json.loads(result.stdout)
	
	print(result.stdout)

	instance_list = output_dict.get('Instances')

	instance_details = instance_list[0]
	
	instance_id = instance_details.get('InstanceId')
	
	describe_instances_command = 'aws ec2 describe-instances --instance-ids' + ' ' + instance_id
	
	#getting public dns
	
	result =subprocess.run([describe_instances_command], shell=True, capture_output=True, text=True)
	
	output_dict = json.loads(result.stdout)
	
	reservations = output_dict.get('Reservations')
	
	instances = reservations[0].get('Instances')
	
	instances_details = instances[0]
	
	publicDnsName = instances_details.get('PublicDnsName')
	
	print(publicDnsName)
	
	#installing ollama + ssh'ing in
	
	sleep(30)
	
	client = SSHClient()
	
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	
	print("attempting to form ssh connection")
	
	client.connect(publicDnsName, username = 'ubuntu', key_filename = 'key.pem')
	
	print('starting install command')
	
	
	run_cmd("curl -fsSL https://ollama.com/install.sh | sh", client)

	# Stop systemd service and disable auto-start
	run_cmd("sudo systemctl stop ollama", client)
	run_cmd("sudo systemctl disable ollama", client)

	# Kill any lingering processes
	run_cmd("pkill -f 'ollama'", client)

	# Start Ollama on 0.0.0.0:11434
	# NOTE: we use a separate shell to launch it in background without PTY issues
	run_cmd("nohup bash -c 'OLLAMA_HOST=0.0.0.0:11434 ollama serve > ollama.log 2>&1  &'", client)

	# Wait a few seconds to let server start
	sleep(5)

	# Check if Ollama is running from inside EC2 (localhost works, not 0.0.0.0)
	run_cmd("curl -s http://localhost:11434 || echo 'Ollama not listening'", client)
	

		#slightly hacky way of making sure that ollama watches port 11434 for requests from all IPs as opposed to only just localhost
	
	sleep(10)
	
	
	base_url = 'http://' + publicDnsName + ":11434" 
	
	model_name = {"name": "orca-mini", "stream": True}
	
	pull_response = pull_model(model_name, base_url)
	print("printing response")
	
	print(pull_response)
	
	model_data = {"model": "orca-mini", "prompt": "describe the mating habits of the stellar's sea lion", "stream": False}
	
	
	while True:
		user_input = input("query: ")
		if user_input == 'quit':
			break
		model_data = {"model": "orca-mini", "prompt": user_input, "stream": False}
		response = generate_response(model_data, base_url)
		print(response["response"])
	
	
	#_stdin, _stdout,_stderr = client.exec_command("curl -fsSL https://ollama.cominstall.sh | sh", get_pty=True)
	#print(_stdout.read().decode())
	#print('installed ollama')
	#then use api from here. for now, i'm going to use hardcoded vals. sue me. 
	#_stdin, _stdout, _stderr = client.exec_command("ollama run llama3", get_pty=True)
	#print('installed llama')
	#_stdin, _stdout, _stderr = client.exec_command("provide a recipe for scrambled eggs", get_pty=True)
	#print('working on command')
	#print(_stdout.read().decode())
	#_stdin.close()
	#client.close()
	terminate_instance(instance_id)
	
	
	
	
except Exception as e: #terminating container when done
	print(traceback.format_exc())
	terminate_instance(instance_id)
	
	

	
	
	






#print(result.stdout)

#result = subprocess.run(['aws ec2 describe-instances'], shell=True, capture_output=True, text=True)

#poopthondict = json.loads(result.stdout)

#print(json.dumps(poopthondict))
