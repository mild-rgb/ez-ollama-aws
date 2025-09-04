This project aims to write a python wrapper library for Boto3, Paramiko, and a few others. It will simplify the running of Ubuntu EC2 instances. All asynchronous functions are wrapped into synchronous ones. This avoids having to write custom logic for each mount/demount operation. For example, .create_disk() will only return when the created disk can be safely mounted. 

I'm also using this library to automate running Ollama/OpenWebUI. 

TODO: Write a proper README
