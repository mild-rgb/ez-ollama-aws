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
3) move your aws key into the folder. use the name for the key that you used to generate it
4) change the 'key name' value in boto_commands to your key name
5) configure the values for model name and desired amazon instance near the top of the project
6) from the terminal, run 'python3 main_program.py'. do not use '&' afterwards as it'll make terminating the EC2 instance difficult (you'll only have to log onto AWS but that's annoying)

**TODO**

- ~~make instance/model type more easily configurable~~ [done]
- allow all configurable values to be given as parametres when main function is called
- directly include openwebui
- ~~add automatic security group management~~ [done]

**Future Features**

- create a python library?
- open an issue if you think you've thought of anything cool and i'll think about it

**Pre-requisites**

An AWS account and a key.
- How to get an AWS account?
https://docs.aws.amazon.com/accounts/latest/reference/manage-acct-creating.html
- How to get a key? 
https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html

**Helpful but not absolutely essential**
- An AWS GPU quota. Gives you access to EC2 instances with GPUs, which make token generation about 5x faster (from my experiments)
https://docs.aws.amazon.com/servicequotas/latest/userguide/request-quota-increase.html
- If you already have an AWS account that you use for something else, I recommend making a seperate IAMS role for this project and using it only for this. If you have any pre-existing security rules, they might clash with this project's auto-management system. 
