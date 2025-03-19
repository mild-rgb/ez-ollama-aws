import requests
import json 


def pull_model(model_dict, api):
	pull_url = api + "/api/pull"
	headers = {}
	payload = json.dumps(model_dict)
	response = requests.request("POST", pull_url, headers=headers, data=payload)
	return response.text
	
def generate_response(model_data, api):
	generate_api = api + "/api/generate"
	payload = json.dumps(model_data)
	headers = {}
	response = requests.request("POST", generate_api, headers=headers, data=payload)
	response_text = response.text
	response_dict = json.loads(response_text)
	return response_dict
	

