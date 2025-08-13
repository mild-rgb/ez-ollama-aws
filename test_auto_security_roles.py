import boto3 
from requests import get 
ec2client = boto3.client('ec2')



def get_security_groups_with_inbound_rule(api_cidr):
    ec2 = boto3.client('ec2')
    security_groups = []
    next_token = None

    while True:
        params = {
             
        }
        if next_token:
            params['NextToken'] = next_token

        response = ec2.describe_security_groups(GroupNames = ['my-custom-security-group'], **params)
        security_groups.extend(response['SecurityGroups'])

        next_token = response.get('NextToken')
        if not next_token:
            break

    return security_groups
    
if __name__ == '__main__':
 ip = ''
 try:
 	ip = str(get('https://checkip.amazonaws.com').text.strip())
 	ip = ip + "/32"
 except Exception as e:
 	print(e)
 	print("you're not connected to the internet or aws is down")
 
 groups = get_security_groups_with_inbound_rule(ip)
 print(groups)
