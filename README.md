# review from 9 months later. read this first and consider it while assessing the project
I wrote this tool in my free time when I was a college student. It's not production grade software. There are several decisions that I'd make differently if I was writing this again as I appreciate the soft sides of SWE far more. 
1) I'd use Terraform + Packer. I essentially duplicated a lot of the functionality here from scratch. 2 hours of research would have saved me weeks of effort.
2) I'd use a QA methodology that wasn't 'does it look right on my machine?'. The AWS region is hardcoded in some places and read from config in some other places. If anyone changed the value in config, it would have failed weirdly and with no error message.
3) I'd have used a project management methodology that wasn't 'what looks wrong to me at this moment and what am I going to do about it tomorrow?'. While it did give me a functioning product, I could have made something so much better
4) I'd have got regular code reviews from other people or AI. The error handling is ugly and barely functional. It will stop EC2 instances from running for days without your knowledge but it won't give any information about where the error came from. It will shut down the EC2 instance ASAP and never attempt to recover
5) I didn't write tests at all. If I saw something was broken, I fixed it
6) The docs were mostly in my head
7) I wrote this by hand. AI was only used as a Stack Exchange replacement

You should only use this repo to get an idea of my technical instincts. Use RunPod if you actually want to run LLMs you don't have the hardware for.

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
- Access to **G-series EC2 instances** with 4 or more cores(request from AWS at https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-resource-limits.html). Give 'running large langauge models' as the reason. 
- A locally stored **AWS keypair (`.pem`)**  

### Setup (first run)  
1) ```bash
   git clone https://github.com/mild-rgb/ez-ollama-aws
   cd ez-ollama-aws
   pip install -r requirements.txt```
2) Create an AWS account [https://signin.aws.amazon.com/signup?request_type=register]
3) Request an increase in your G-series CPU quota. Give running large langauge models as the reason [https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-resource-limits.html]
4) Create a key pair and download it [https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/create-key-pairs.html]. Place the .pem file in the project folder. If the key name is not 'key', change the 'key_name' field in base_config.json to match. 
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
- [ ] HTTPS? as shown in [https://docs.openwebui.com/tutorials/https-nginx/]
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
