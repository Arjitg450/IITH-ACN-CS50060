import socket
import threading
import os
from queue import Queue

HOST = "127.0.0.2"  # Server's IP address
PORT = 12345  # Port to listen on
# WEB_ROOT = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the server script


def handle_server(path, server_add, server_port, queue):
    # Create a new socket for each request
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((server_add, server_port))
    print(f"[CONNECTED] Connected to the server on ('{server_add},{server_port}')")

    # Construct and send the HTTP GET request
    request = f"GET {path} HTTP/1.1\r\nHost: {server_add}\r\nConnection: close\r\n\r\n"
    server_socket.send(request.encode())

    # Receive and display the response
    response = b""
    while True:
        data = server_socket.recv(1024)
        if not data:
            break
        response += data

    server_socket.close()
    queue.put(response)


def handle_client(client_socket):
    request_data = client_socket.recv(1024).decode()

    # Parse the HTTP request
    request_lines = request_data.split("\n")
    request_line = request_lines[0]
    method, path, _ = request_line.split()
    request_line = request_lines[1]
    _, server_add = request_line.split()
    request_line = request_lines[2]
    _, server_port = request_line.split()
    server_port = int(server_port)

    # Create a Queue to store the result
    result_queue = Queue()

    # Create a thread to connect Server
    server_thread = threading.Thread(
        target=handle_server, args=(path, server_add, server_port, result_queue)
    )
    server_thread.start()

    # Wait for the thread to finish
    server_thread.join()

    response = result_queue.get()
    client_socket.send(response)
    client_socket.close()


def start_proxy_server():
    proxy_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_server_socket.bind((HOST, PORT))
    proxy_server_socket.listen(5)
    print(f"[LISTENING] Web ProxyServer is listening on {HOST}:{PORT}")

    while True:
        client_socket, client_address = proxy_server_socket.accept()
        print(f"[CONNECTED] Accepted connection from {client_address}")

        # Create a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()


if __name__ == "__main__":
    start_proxy_server()
