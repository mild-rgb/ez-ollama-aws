import traceback
from paramiko import SSHClient
import paramiko
from time import sleep
from util_functions import *
from commands import *
from setupparams import params
instance_id = ''
configjsonhandler = JsonHandler("base_config.json")
datajsonhandler = JsonHandler("data.json")
resource = boto3.resource('ec2', region_name = configjsonhandler.get("region"))
client = boto3.client('ec2', region_name = configjsonhandler.get("region"))
networkmanager = AWSNetworkManager(client)

try:

    instance_type = configjsonhandler.get("instance_type")

    key_name = configjsonhandler.get("key_name")

    image_id = configjsonhandler.get("base_ami_id")

    #investigate iams

    security_group_id = networkmanager.get_security_group()

    exit()

    params['TagSpecifications'][0]['Tags'][0]['Value'] = str(time.time())
    params['NetworkInterfaces'][0]['Groups'] = [security_group_id]
    params['InstanceType'] = instance_type
    params['KeyName'] = key_name
    params['ImageId'] = image_id


    instance = resource.create_instances(**params)

# end startinstance

    instance = instance[0]

    instance.wait_until_running()

    instance.load()

# start RunCMD

    instance_id = instance.id

    device_name = instance.block_device_mappings[0]['DeviceName']

    public_dns_name = instance.public_dns_name

    print(instance_id)

    sleep(10) #waiting for instance to be ready

    sshclient = SSHClient()

    sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print("attempting to form ssh connection")

    key_filename = key_name + ".pem"

    sshclient.connect(public_dns_name, username = 'ubuntu', key_filename = key_filename)

    run_cmd = RunCMD(sshclient)

# end RunCMD

    run_cmd.execute("echo 'hello world'")

    ebs_id = create_ebs_disk(client) #maybe wrap this into another object?

    waiter = client.get_waiter('volume_available')

    waiter.wait(VolumeIds=[ebs_id])

    response = instance.attach_volume(
        Device = '/dev/sdf',
        VolumeId = ebs_id,
        )

    run_cmd.exec_until_no_error(format_and_mount, 'mke2fs 1.47.0 (5-Feb-2023)', delay=10) # because it takes time for the volume to mount

    run_cmd.make_folder('/home/ubuntu/mnt', 'ollama_stuff')

    run_cmd.make_folder('/home/ubuntu/mnt', 'docker')

    run_cmd.execute('cd /home/ubuntu/mnt && ls')

    run_cmd.execute(install_ollama)

    run_cmd.execute('sudo chmod -R 777 /home/ubuntu/')

    run_cmd.overwrite_systemd_file('ollama.service', ollama_service)

    run_cmd.execute('ollama pull gemma3:12b')

    run_cmd.execute('cd /home/ubuntu/mnt/ollama_stuff && ls')

    run_cmd.execute(install_docker)
    
    run_cmd.execute('sudo systemctl stop docker')

    run_cmd.make_file_and_write_in('/etc/docker', 'daemon.json', docker_newloc)

    run_cmd.execute('sudo systemctl daemon-reexec && sudo systemctl start docker')

    run_cmd.make_folder('/home/ubuntu/', 'scripts')

    run_cmd.make_exec('/home/ubuntu/scripts/', 'startuiscript.sh', startuiscript)

    run_cmd.make_exec('/home/ubuntu/scripts/', 'mountscript.sh', automountscript)

    run_cmd.execute('sudo touch /home/ubuntu/scripts/mounted')

    run_cmd.make_file_and_write_in('/etc/systemd/system/', 'automount.service', automount)

    run_cmd.make_file_and_write_in('/etc/systemd/system/', 'startui.service' , startui)

    run_cmd.execute('sudo systemctl daemon-reload')

    run_cmd.execute('sudo bash /home/ubuntu/scripts/startuiscript.sh')

    run_cmd.execute('sudo systemctl enable startui.service')

    run_cmd.execute('sudo systemctl enable automount.service')

    run_cmd.execute('sudo rm /home/ubuntu/scripts/mounted')

    client.detach_volume(
        VolumeId=ebs_id,
    )


    waiter = client.get_waiter('volume_available')

    waiter.wait(VolumeIds=[ebs_id])

    print(response)

#start create image

    response = client.create_image(
        InstanceId=instance_id,
            Name=str(time.time()),
            Description='Baked AMI from instance',
            NoReboot=False  # Set to False if you want to ensure file system consistency
    )

# Extract the new AMI ID
    ami_id = response['ImageId']

    print(ami_id)

    print(ebs_id)

    datajsonhandler.set('ami_id', ami_id)
    datajsonhandler.set('ebs_id', ebs_id)

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

# end create image

    print(client.terminate_instances(InstanceIds=[instance_id]))

except KeyboardInterrupt:
    print(client.terminate_instances(InstanceIds=[instance_id]))
finally: #terminating container when done
    print(client.terminate_instances(InstanceIds=[instance_id]))
    print(traceback.format_exc())

    '''
 groups = get_security_groups_with_inbound_rule(ip)
 print(groups)
 '''

