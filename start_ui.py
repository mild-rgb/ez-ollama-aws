import docker
from docker.types import Mount

def start_container(ec2_address):
    """Starts the Open-WebUI container with specified configuration"""
    client = docker.from_env()
    
    # Remove existing container if it exists
    try:
        existing_container = client.containers.get('open-webui')
        existing_container.remove(force=True)
    except docker.errors.NotFound:
        pass
    
    # Start fresh container
    container = client.containers.run(
    "ghcr.io/open-webui/open-webui:main",
    detach=True,
    network_mode="host",  # Equivalent to --network=host
    volumes={"open-webui": {"bind": "/app/backend/data", "mode": "rw"}},
    environment={"OLLAMA_BASE_URL": ec2_address},
    name="open-webui",
    restart_policy={"Name": "always"}  # Equivalent to --restart always
    )
    container.start()
    print("Container started successfully")

def stop_container():
    """Stops and removes the Open-WebUI container"""
    client = docker.from_env()
    
    try:
        container = client.containers.get('open-webui')
        container.stop()
        container.remove()
        print("Container stopped and removed")
    except docker.errors.NotFound:
        print("Container not found")
