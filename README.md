**ez-ollama-aws**

ez-ollama-aws is a project that aims to provide command-line levels of abstraction over AWS EC2 instances running ollama.

With one python script executed from the command line, it sets up an AWS EC2 instance, connects to the instance, installs ollama on the instance and then connects to the api. The EC2 instance is automatically terminated by the program when a keyboard interrupt is passed. 



**Current Features** 

- initialisation and installation of gemma3-12b on a c4.2xlarge instance through just one terminal command
- prompt model and recieve responses from the command line
- automatically shuts down instance when program is closed [no eating ramen for a week because you forgot to shut down your instance before going on holiday]

**How to use / configure**

Configure 


0) if you already have an AWS account, consider setting up an IAM role solely for this project. it will automatically parse and create security roles, which may clash with whatever you already have running
1) create an AWS account (helpful link here - https://docs.aws.amazon.com/accounts/latest/reference/manage-acct-creating.html)
2) set up access keys and make a note of them (https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html)
3) create a key pair (https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/create-key-pairs.html#having-ec2-create-your-key-pair)
4) run 'aws configure' in the same terminal. insert your access keys.
5) move the .pem file that you made while setting up your access keys into the folder. use the name for the key filename that you used to generate it
6) set values for instance_type, key_name, and model_name in main_program.py. default values are model_name = "gemma3:12b", instance_type = "c5.2xlarge", and key_name = 'laptop_key'
7) [optional but strongly recommended for better generation speeds] get a quota increase to allow you to use instances with GPUs (https://docs.aws.amazon.com/servicequotas/latest/userguide/request-quota-increase.html)

Run

1) from the terminal, run 'python3 main_program.py'. do not use '&' afterwards as it'll make terminating the EC2 instance difficult (you'll only have to log onto AWS but that's annoying)

**TODO**

- ~~make instance/model type more easily configurable~~ [done]
- allow all configurable values to be given as parametres when main function is called
- directly include openwebui [set up reverse proxy on localhost to handle communication with aws]
- use a more secure way of connecting to ec2 - aws warns against my current approach [update - implement ec2 secure connect]
- investigate using spot instances [possibly have user define a range of acceptable instances or give some model parametres and auto match a range?]
- ~~add automatic security group management~~ [done]

**Future Features**

- create a python library?
- open an issue if you think you've thought of anything cool and i'll think about it
