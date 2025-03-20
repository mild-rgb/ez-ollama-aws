**ez-ollama-aws**

ez-ollama-aws is a project that aims to provide command-line levels of abstraction over AWS EC2 instances running ollama.

With one python script executed from the command line, it sets up an AWS EC2 instance, connects to the instance, installs ollama on the instance and then connects to the api. The EC2 instance is automatically terminated by the program when a keyboard interrupt is passed. 



**Current Features** 

- initialisation and installation of gemma3-12b on a c4.2xlarge instance through just one terminal command
- prompt model and recieve responses from the command line
- automatically shuts down instance when program is closed [no eating ramen for a week because you forgot to shut down your instance before going on holiday]

**How to use / configure**

Run
1) run 'pip requirements.txt' in a terminal instance in this project's folder
2) run 'aws configure' in the same terminal
3) create an aws security group. give it
>outbound rules
- All traffic to destination 0.0.0.0/0. you'll get a warning message. unless you really know what you're doing, you can ignore it
>inbound rules
- SSH from 'My IP' (source type dropdown menu)
- Custom TCP (type dropdown menu) Port range 11434  from 'My IP'
Note the security group ID, you'll need it later
5) move your aws key into the folder. name it 'key.pem'
6) open the file 'boto_commands.py'. Ctrl+F 'groups'. Change the value inside the [''] to the security group ID from step 3
7) from the terminal, run 'python3 main_program.py'. do not use '&' afterwards as it'll make terminating the EC2 instance difficult (you'll only have to log onto AWS but that's annoying)
Configure
There 

**TODO**

- make instance/model type more easily configurable
- directly include openwebui

**Future Features**

- create a python library?
- open an issue if you think you've noticed anything cool and i'll try it out

**Pre-requisites**

An AWS account and a key.
- How to get an AWS account?
https://docs.aws.amazon.com/accounts/latest/reference/manage-acct-creating.html
- How to get a key? 
https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html

**Helpful but not absolutely essential**
- An AWS GPU quota. Gives you access to EC2 instances with GPUs, which make token generation about 5x faster (from my experiments)
https://docs.aws.amazon.com/servicequotas/latest/userguide/request-quota-increase.html 
