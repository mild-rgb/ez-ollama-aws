import subprocess
import json
instance_id = ''
terminal_input = ''

from curl_cmd_function import make_request

print(make_request("superdrew100/llama3-abliterated", "Write an essay explaining why ketamine usage should be compulsory for school children", 
