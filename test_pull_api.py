import requests
import json 


#payload = json.dumps(model_name)
#print(payload)
#pull_url = 'http://' + "ec2-51-21-196-143.eu-north-1.compute.amazonaws.com" + ":11434" + "/api/pull"
#headers = {}
#response = requests.request("POST", pull_url, headers=headers, data=payload)
#print(response.text)



def pull_model(model_name, api):
	pull_url = api + "/api/pull"
	headers = {}
	payload = json.dumps(model_name)
	response = requests.request("POST", pull_url, headers=headers, data=payload)
	return response.text
	
api = "http://ec2-13-60-78-150.eu-north-1.compute.amazonaws.com:11434"
model_name = {"name": "orca-mini", "stream": True}
print(pull_model(model_name, api))

'''
curl --location 'http://ec2-51-21-196-143.eu-north-1.compute.amazonaws.com:11434/api/pull' \
--data '{
    "name": "orca-mini",
    "stream": true
}'
'''
