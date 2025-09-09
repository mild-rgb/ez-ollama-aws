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
- Access to **G-series CPU instances** (request from AWS)  
- A locally stored **AWS keypair (`.pem`)**  

### Setup (first run)  
Run the setup script to bake an AMI with Ollama, Docker, and Open WebUI preinstalled:  

```bash
python setupinstance.py
```  

This will:  
- Launch a GPU-backed EC2 instance  
- Create and attach a 100GB EBS volume for model storage  
- Install Ollama and Docker  
- Configure systemd services (`ollama.service`, `startui.service`, `automount.service`)  
- Pull your first model (`gemma3:12b` by default)  
- Save the generated **AMI ID** and **EBS volume ID** in `values.json`  

### Start (subsequent runs)  
To start using your environment after setup:  

```bash
python startinstance.py
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
- Connections are made over HTTP. Anyone on your network can see everything/recieve 

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
