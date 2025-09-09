format_and_mount =  """
DEVICE=/dev/$(lsblk | grep '100G' | awk '{print $1}')&&
sudo udevadm settle &&
sleep 5 &&
sudo wipefs -af $DEVICE &&
sudo parted --script $DEVICE mklabel gpt mkpart primary ext4 0% 100% &&
sudo partprobe $DEVICE &&
sleep 2 &&
sudo mkfs.ext4 ${DEVICE}p1 &&
sudo mkdir -p /home/ubuntu/mnt &&
sudo mount ${DEVICE}p1 /home/ubuntu/mnt
"""


install_ollama = 'curl -fsSL https://ollama.com/install.sh | sh'

install_docker = """sudo apt-get update && \
sudo apt-get install -y ca-certificates curl && \
sudo install -m 0755 -d /etc/apt/keyrings && \
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc && \
sudo chmod a+r /etc/apt/keyrings/docker.asc && \
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
https://download.docker.com/linux/ubuntu \
$(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null && \
sudo apt-get update && \
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
"""


go_to_systemd = 'cd . && cd ../../etc/systemd/system'

docker_newloc = """
{
  "data-root": "/home/ubuntu/mnt/docker" 
}
"""

automountscript = """#!/bin/bash
device="/dev/$(lsblk -ndo NAME,SIZE | grep '100G' | awk '{print $1}')p1"
# Check if the device is mounted
if findmnt -nr -o target -S "$device" > /dev/null; then
    exit 0
else
    mount "$device" /home/ubuntu/mnt && touch /home/ubuntu/scripts/mounted
fi
"""

startuiscript = """#!/bin/bash
while [ ! -e "/home/ubuntu/scripts/mounted" ]; do
  echo "Waiting for disk to mount"
  sleep 
done
systemctl restart docker.service && docker run -d --network=host \
  -v open-webui:/app/backend/data \
  -e OLLAMA_BASE_URL=http://127.0.0.1:11434 \
  --name open-webui \
  --restart always \
  ghcr.io/open-webui/open-webui:main
"""


automount = """
[Unit]
Description=Mount Device Script
After=network.target

[Service]
ExecStart=/home/ubuntu/scripts/mountscript.sh
Restart=on-failure
RestartSec=3

[Install]
WantedBy=multi-user.target
"""
startui = """
[Unit]
Description=start ui script
After=network.target

[Service]
Type=oneshot
ExecStart=/home/ubuntu/scripts/startuiscript.sh

[Install]
WantedBy=multi-user.target
"""

ollama_service = """
[Unit]
Description=Ollama Service
After=network-online.target

[Service]
ExecStart=/usr/local/bin/ollama serve
User=ollama
Group=ollama
Restart=always
RestartSec=3
Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin"
Environment="OLLAMA_MODELS=/home/ubuntu/mnt/ollama_stuff"

[Install]
WantedBy=default.target"""