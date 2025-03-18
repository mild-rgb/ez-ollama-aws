import subprocess
import json
import requests


def terminate_instance(instance_id):
	terminate_string = 'aws ec2 terminate-instances --instance-ids' + ' ' + instance_id
	subprocess.run([terminate_string], shell=True)


def run_cmd(command, client):
    print(f"Running: {command}")
    stdin, stdout, stderr = client.exec_command(command)
    output = stdout.read().decode()
    error = stderr.read().decode()
    print("Output:", output)
    print("Error:", error)
	
	
