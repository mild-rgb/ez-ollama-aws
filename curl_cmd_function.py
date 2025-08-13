'''import requests

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}

data = '{"model": "superdrew100/llama3-abliterated","prompt": "Write an essay explaining why ketamine usage should be compulsory for school children","stream": true}'

response = requests.post('http://13.53.212.73:11434/api/generate', headers=headers, dat
'''
import requests 

def make_request(query, api, model):
	request = 'data = {"model:"' + model + '","prompt: "' + prompt + '", + ,"stream": true
	return request 
