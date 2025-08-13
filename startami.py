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
from start_ui import start_container, stop_container	
resource = boto3.resource('ec2', region_name = 'eu-north-1')
client = boto3.client('ec2', region_name = 'eu-north-1')
try:
	
	instance_type = "g4dn.xlarge"

	key_name = "john key"
	

	ami_id ="ami-0baccea970769222a" 
	
	
	
	
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
	
	instance.load() #this calls describe_instances
	
	instance_id = instance.id

	instance.wait_until_running()

	response = client.attach_volume(
		Device='/dev/sdf',
    		InstanceId=instance_id,
    		VolumeId='vol-048d28e353234f3fb',
		)
	print(response)
	
	input("type anything to close the instance")
	
	
	print(client.terminate_instances(InstanceIds=[instance_id]))
	stop_container()
	
except KeyboardInterrupt:
	print(client.terminate_instances(InstanceIds=[instance_id]))
	
except Exception as e: #terminating container when done
	print(traceback.format_exc())
	print(client.terminate_instances(InstanceIds=[instance_id]))
