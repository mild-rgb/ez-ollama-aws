params = {
    'ImageId': 'ami-0c1ac8a41498c1a9c',
    'InstanceType': 'c5.2xlarge',
    'KeyName': 'laptop_key',
    'BlockDeviceMappings': [
        {
            'DeviceName': '/dev/sda1',
            'Ebs': {
                'Encrypted': False,
                'DeleteOnTermination': True,
                'Iops': 3000,
                'VolumeSize': 26,
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
    'MinCount': 1,
    'MaxCount': 1
}
