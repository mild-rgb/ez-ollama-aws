params = {
    'ImageId': '',
    'InstanceType': '',
    'KeyName': 'key',
    'BlockDeviceMappings': [
        {
            'DeviceName': '/dev/sda1',
            'Ebs': {
                'Encrypted': False,
                'DeleteOnTermination': True,
                'Iops': 3000,
                'VolumeSize': 15,
                'VolumeType': 'gp3',
                'Throughput': 125
            }
        }
    ],
    'NetworkInterfaces': [
        {
            'AssociatePublicIpAddress': True,
            'DeviceIndex': 0,
            'Groups': ''
        }
    ],
    'MetadataOptions': {
        'HttpEndpoint': 'enabled',
        'HttpPutResponseHopLimit': 2,
        'HttpTokens': 'required'
    },
    'PrivateDnsNameOptions': {
        'HostnameType': 'ip-name',
        'EnableResourceNameDnsARecord': True,
        'EnableResourceNameDnsAAAARecord': False
    },
    'TagSpecifications': [
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'MyInstanceName'
                }
            ]
        }
    ],
    'Placement': {
        'AvailabilityZone': 'eu-north-1b'
    },
    'MinCount': 1,
    'MaxCount': 1
}

