from setupinstance import networkmanager
from setupparams import params
from util_functions import *
import traceback
from time import sleep
import webbrowser

resource = boto3.resource('ec2', region_name = 'eu-north-1')
client = boto3.client('ec2', region_name = 'eu-north-1')
networkmanager = AWSNetworkManager(client)
instance_id=''
ebs_id = ''

try: 
    base_config = JsonHandler('base_config.json')
    data = JsonHandler('data.json')
    ami_id = data.get('ami_id')
    ebs_id = data.get('ebs_id')
    print(ami_id)
    instance_type = base_config.get("instance_type")
    key_name = base_config.get("key_name")
    unique_name = str(time.time())

    #turn all of this into a function
    local_ip = get_local_ip()

    vpc_id = get_vpc_id(client)
    security_group_id = networkmanager.create_and_configure_security_group(unique_name, vpc_id, local_ip, client)

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
    sleep(70)

    print(public_dns_name)
    public_dns_name = "http:" + public_dns_name + ":8080"
    webbrowser.open(public_dns_name)
    input("type anything to close the instance")
    client.detach_volume(VolumeId=ebs_id, )
    print(client.terminate_instances(InstanceIds=[instance_id]))





except KeyboardInterrupt:
    print(client.detach_volume(VolumeId=ebs_id,))
    print(client.terminate_instances(InstanceIds=[instance_id]))
except Exception as e: #terminating container when done
    print(client.detach_volume(VolumeId=ebs_id,))
    print(client.terminate_instances(InstanceIds=[instance_id]))
    print(traceback.format_exc())

