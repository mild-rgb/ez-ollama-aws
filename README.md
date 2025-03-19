**ez-ollama-aws**

ez-ollama-aws is a project that aims to provide command-line levels of control over ollama running on AWS.

With one python script executed from the command line, it sets up an AWS EC2 instance, connects to it, installs  



**Current Features** 
- initialisation and installation of orca-mini on a c4.2xlarge instance through just one terminal command
- prompt model and recieve responses from the command line
- automatically shuts down instance when program is closed [no eating ramen for a week because you forgot to shut down your instance before going on holiday] 

**Future Features** 
- reverse ollama API proxy - allows integration with tools that assume ollama is locally installed
- commandline choice of models 


**TODO**
- implement support for chat history 
- implement support for multimodal models 
- add more information about model generation

**Pre-requisites**
An AWS account and a key.
- How to get an AWS account?
https://docs.aws.amazon.com/accounts/latest/reference/manage-acct-creating.html
- How to get a key? 
https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html
 
