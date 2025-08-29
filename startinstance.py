from boto_commands import *
from util_functions import *
import traceback
from time import sleep
import webbrowser

resource = boto3.resource('ec2', region_name = 'eu-north-1')
client = boto3.client('ec2', region_name = 'eu-north-1')
instance_id=''
try: 
	jsonhandler = JsonHandler()
	ami_id = jsonhandler.get('ami_id')
	ebs_id = jsonhandler.get('ebs_id')
	print(ami_id)
	instance_type = "g4dn.xlarge" #use a single source of truth for key_name and instance_type
	key_name = "key"
	unique_name = str(time.time())

	#turn all of this into a function
	local_ip = get_local_ip()

	vpc_id = get_vpc_id(client)
	security_group_id = create_and_configure_security_group(unique_name, vpc_id, local_ip, client)

	params['ImageId'] = ami_id
	params['TagSpecifications'][0]['Tags'][0]['Value'] = unique_name
	params['NetworkInterfaces'][0]['Groups'] = [security_group_id]
	params['InstanceType'] = instance_type
	params['KeyName'] = key_name

	instance = resource.create_instances(**params)
	print("created instance")        
	instance = instance[0]
	instance.wait_until_running()
	print("instance running")
	instance.load()
	instance_id = instance.id
	device_name = instance.block_device_mappings[0]['DeviceName']
	public_dns_name = instance.public_dns_name
	print("mounting disk")
	response = client.attach_volume(
		Device = '/dev/sdg',
		InstanceId = instance_id,
		VolumeId = ebs_id
	)
	print("mounted disk")
	sleep(20)
	
	print(public_dns_name)
	public_dns_name = "http:" + public_dns_name + ":3000"
	webbrowser.open(public_dns_name)
	input("type anything to close the instance")
	print(client.terminate_instances(InstanceIds=[instance_id]))
	response = client.detach_volume(VolumeId=ebs_id,)
	
	
	
	
except KeyboardInterrupt:
	print(client.terminate_instances(InstanceIds=[instance_id]))
	response = client.detach_volume(VolumeId=ebs_id,)
except Exception as e: #terminating container when done
	print(client.terminate_instances(InstanceIds=[instance_id]))
	response = client.detach_volume(VolumeId=ebs_id,)
	print(traceback.format_exc())

