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
from setupparams import params
instance_id = ''
url = ''
user_input = ''
security_group_id = ''
resource = boto3.resource('ec2', region_name = 'eu-north-1')
client = boto3.client('ec2', region_name = 'eu-north-1')
jsonhandler = JsonHandler()
try:
	
	#configs - make these be taken through cmd line
	
	instance_type = "g4dn.xlarge"

	key_name = "jackkey"

	unique_name = str(time.time())
	
	local_ip = get_local_ip()
	
	print(local_ip)

	#security_group_list = get_security_groups_with_inbound_rule(local_ip, client)

	#print(security_group_list)
	

	vpc_id = get_vpc_id(client)
	security_group_id = create_and_configure_security_group(unique_name, vpc_id, local_ip, client)
	
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

	
	device_name = instance.block_device_mappings[0]['DeviceName']

	public_dns_name = instance.public_dns_name
	
	print(public_dns_name)
	
	print(instance_id)
	
	sleep(10) #waiting for instance to be ready
	
	sshclient = SSHClient()
	
	sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	
	print("attempting to form ssh connection")
	
	key_filename = key_name + ".pem"
	
	sshclient.connect(public_dns_name, username = 'ubuntu', key_filename = key_filename)

	run_cmd = RunCMD(sshclient)
	
	

	#run_cmd("echo 'hello world'", sshclient)
	run_cmd.execute("echo 'hello world'")

	ebs_id = create_ebs_disk(client)

	#save ebs id to params when automount is done

	#print(ebs_id)

	waiter = client.get_waiter('volume_available')

	waiter.wait(VolumeIds=[ebs_id])

	response = client.attach_volume(
		Device = '/dev/sdf',
    		InstanceId = instance_id,
    		VolumeId = ebs_id,
		)

	#print(response)

	#waiter = client.get_waiter('volume_in_use')

	#waiter.wait(VolumeIds=[ebs_id])

	run_cmd.exec_until_no_error(format_and_mount, 'mke2fs 1.47.0 (5-Feb-2023)', delay=10) 

	#run_cmd(format_and_mount, sshclient)

	run_cmd.make_folder('/home/ubuntu/mnt', 'ollama_stuff')

	run_cmd.make_folder('/home/ubuntu/mnt', 'docker_stuff')

	#run_cmd('cd . && cd mnt && sudo mkdir ollama_stuff && sudo mkdir docker_stuff', sshclient)

	run_cmd.execute('cd /home/ubuntu/mnt && ls')

	#run_cmd('touch test.txt', sshclient)

	#insert_text_into_file('мир, иди нахуй', 'test.txt', sshclient)

	#run_cmd('cat test.txt', sshclient)

	run_cmd.execute(install_ollama)

	run_cmd.execute('sudo chmod -R 777 /home/ubuntu/') #permissions will be restricted later but this is faster

	run_cmd.overwrite_systemd_file('ollama.service', ollama_service)

	run_cmd.execute('ollama pull gemma3:12b')

  	#run_cmd('ollama pull gemma3:12b-it-qat', sshclient)

	run_cmd.execute('cd /home/ubuntu/mnt/ollama_stuff && ls')

	run_cmd.execute(install_docker)

	run_cmd.make_file_and_write_in('/etc/docker', 'docker.json', docker_newloc)

	run_cmd.make_folder('/home/ubuntu/', 'scripts')

	run_cmd.make_exec('/home/ubuntu/scripts/', 'startuiscript.sh', startuiscript)

	run_cmd.make_exec('/home/ubuntu/scripts/', 'mountscript.sh', automountscript)

	run_cmd.make_file_and_write_in('/etc/systemd/system/', 'automount.service', automount)

	run_cmd.make_file_and_write_in('/etc/systemd/system/', 'startui.service' , startui)

	run_cmd.execute('sudo systemctl daemon-reload')

	run_cmd.execute('sudo systemctl start startui.service')

	run_cmd.execute('sudo systemctl start automount.service')

	run_cmd.execute('sudo systemctl enable startui.service')

	run_cmd.execute('sudo systemctl enable automount.service')

	response = client.detach_volume(
		VolumeId=ebs_id,
	)


	waiter = client.get_waiter('volume_available')

	waiter.wait(VolumeIds=[ebs_id])

	print(response)

	response = client.create_image(
		InstanceId=instance_id,
    		Name=unique_name,
    		Description='Baked AMI from instance',
    		NoReboot=False  # Set to False if you want to ensure file system consistency
	)

# Extract the new AMI ID
	ami_id = response['ImageId']

	print(ami_id)

	print(ebs_id)

	jsonhandler.set('ami_id', ami_id)

	jsonhandler.set('ebs_id', ebs_id)
	
	while True:
		response = client.describe_images(ImageIds=[ami_id])
		state = response['Images'][0]['State']
		print(f"Current image state: {state}")
		if state == 'available':
			print("AMI is ready!")
			break
		elif state == 'failed':
			print("AMI creation failed.")
			break
		time.sleep(15)  # wait before checking again

	print(client.terminate_instances(InstanceIds=[instance_id]))

except KeyboardInterrupt:
	print(client.terminate_instances(InstanceIds=[instance_id]))
except Exception as e: #terminating container when done
	print(client.terminate_instances(InstanceIds=[instance_id]))
	print(traceback.format_exc())

	'''
 groups = get_security_groups_with_inbound_rule(ip)
 print(groups)
 '''
	
