# ez-ollama-aws  

Run [Ollama](https://ollama.ai) + [Open WebUI](https://github.com/open-webui/open-webui) on AWS GPU instances with **persistent storage and near-local latency**, even if your own hardware can’t handle large LLMs.  

## Features  
- Launch an AWS GPU instance preloaded with **Ollama** and **Open WebUI**  
- Automatic **EBS volume management** for persistent model storage  
- From cold start → usable WebUI in about 70 seconds  
- Security group setup so only your IP can access the instance  
- Creates and reuses a custom AMI for faster future launches  
- Provides systemd services for automatic Ollama and WebUI startup  

## Getting Started  

### Prerequisites  
- An **AWS account**  
- Access to **G-series CPU instances** (request from AWS at https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-resource-limits.html)  
- A locally stored **AWS keypair (`.pem`)**  

### Setup (first run)  
1) ```bash
   git clone https://github.com/mild-rgb/ez-ollama-aws
   cd ez-ollama-aws
   pip install requirements.txt```
2) Create an AWS account [https://signin.aws.amazon.com/signup?request_type=register]
3) Request access to G-series instances [https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-resource-limits.html]
4) Create a key pair and download it []https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/create-key-pairs.html. Place the .pem file in the project folder. If the key name is not 'key', change the 'key_name' field in base_config.json to match. 
5) ```bash
       python3 setupinstance.py
   ```
6) Wait for setupinstance.py to finish running. It will print 'AMI is ready!' when it is done


This will:  
- Launch a GPU-backed EC2 instance  
- Create and attach a 100GB EBS volume for model storage  
- Install Ollama and Docker  
- Configure systemd services (`ollama.service`, `startui.service`, `automount.service`)  
- Pull your first model (`gemma3:12b` by default)  
- Save the generated **AMI ID** and **EBS volume ID** in `values.json`  

### Use (after setup)
1) ```bash 
      python3 run.py
   ```

This will:  
- Launch a new instance from the saved AMI  
- Reattach the EBS disk (with your models)  
- Restart Ollama and Open WebUI automatically  
- Open the WebUI in your default browser (`http://<instance-public-dns>:8080`)  

When finished, just stop the instance from your terminal and it will detach the volume and terminate cleanly.  

## Tech Stack  
- **Language:** Python 3.10  
- **AWS SDK:** [boto3](https://boto3.amazonaws.com/)  
- **SSH & Remote Exec:** [paramiko](http://www.paramiko.org/)  
- **Infra:** AWS EC2 G-series GPU instances, EBS for persistent storage  

## Roadmap  
- [ ] Abstract EC2 + EBS orchestration into a proper Python library
- [ ] Cost monitoring / auto-shutdown helpers  

## Security Notes  
- API keys or AWS credentials should be handled via **environment variables** (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`).  
- Connections are made over HTTP. Anyone on your network can see everything you send/recieve
## License  
This project is licensed under the [MIT License](LICENSE).  

## Acknowledgments  
Shoutouts to:  
- [Ollama](https://ollama.ai)  
- [Open WebUI](https://github.com/open-webui/open-webui)  
- [AWS](https://aws.amazon.com)  

## Badges  
- ![Python](https://img.shields.io/badge/python-3.10-blue)  
- ![License](https://img.shields.io/badge/license-MIT-green)  
