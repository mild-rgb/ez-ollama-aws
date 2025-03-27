import socket
import threading
import sys

def forward(src, dst):
    """Continuously forward data from src to dst."""
    try:
        while True:
            data = src.recv(4096)
            if not data:
                break
            dst.sendall(data)
    except Exception as e:
        print(f"Forwarding error: {e}")
    finally:
        src.close()
        dst.close()

def handle_client(client_socket, remote_host, remote_port):
    """Handles an incoming connection by setting up a connection to the remote host."""
    try:
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((remote_host, remote_port))
    except Exception as e:
        print(f"Could not connect to remote {remote_host}:{remote_port} - {e}")
        client_socket.close()
        return

    # Create two threads to forward data in both directions
    t1 = threading.Thread(target=forward, args=(client_socket, remote_socket))
    t2 = threading.Thread(target=forward, args=(remote_socket, client_socket))
    t1.start()
    t2.start()

def main():
    if len(sys.argv) != 4:
        print("Usage: python port_forwarder.py <local_port> <remote_host> <remote_port>")
        sys.exit(1)

    local_port = int(sys.argv[1])
    remote_host = sys.argv[2]
    remote_port = int(sys.argv[3])

    # Create a socket to listen for incoming connections on localhost
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('localhost', local_port))
        server.listen(5)
        print(f"Listening on localhost:{local_port} and forwarding to {remote_host}:{remote_port}")
    except Exception as e:
        print(f"Could not bind to port {local_port}: {e}")
        sys.exit(1)

    while True:
        try:
            client_socket, addr = server.accept()
            print(f"Accepted connection from {addr}")
            client_thread = threading.Thread(target=handle_client, args=(client_socket, remote_host, remote_port))
            client_thread.daemon = True  # Optional: makes threads exit when main thread exits
            client_thread.start()
        except KeyboardInterrupt:
            print("Shutting down the server.")
            break
        except Exception as e:
            print(f"Error accepting connection: {e}")

if __name__ == '__main__':
    main()
