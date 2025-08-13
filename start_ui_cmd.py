
import docker

client = docker.from_env()

try:
        existing_container = client.containers.get('open-webui')
        existing_container.remove(force=True)
except docker.errors.NotFound:
        pass

container = client.containers.run(
    "ghcr.io/open-webui/open-webui:main",
    detach=True,
    network_mode="host",  # Equivalent to --network=host
    volumes={"open-webui": {"bind": "/app/backend/data", "mode": "rw"}},
    environment={"OLLAMA_BASE_URL": "http://127.0.0.1:11434"},
    name="open-webui",
    restart_policy={"Name": "always"}  # Equivalent to --restart always
)



input("type anything to end the container (rightly)")

    
try:
        container = client.containers.get('open-webui')
        container.stop()
        container.remove()
        print("Container stopped and removed")
except docker.errors.NotFound:
        print("Container not found")

print(f"Container {container.short_id} started successfully!")
