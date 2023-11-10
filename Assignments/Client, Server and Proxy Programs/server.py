import socket
import threading
import os

HOST = '127.0.0.3'  # Server's IP address
PORT = 15200      # Port to listen on
WEB_ROOT = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the server script

def handle_client(client_socket):
    request_data = client_socket.recv(1024).decode()
    
    # Parse the HTTP request
    request_lines = request_data.split('\n')
    request_line = request_lines[0]
    method, path, _ = request_line.split()
    
    # print(path)
    # print()

    # Check if the requested file exists
    file_path = path.lstrip('/')
    if os.path.isfile(file_path):
        # Read the content of the requested file
        with open(file_path, 'rb') as file:
            response_data = file.read()
        response_headers = f"HTTP/1.1 200 OK\nContent-Length: {len(response_data)}\n\n".encode()
    else:
        # If the file is not found, send a 404 response
        response_data = "File Not Found".encode()
        response_headers = f"HTTP/1.1 404 Not Found\nContent-Length: {len(response_data)}\n\n".encode()
    
    # Send the response to the client
    response = response_headers + response_data
    
    client_socket.send(response)
    
    client_socket.close()



def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"[CONNECTED] Accepted connection from {client_address}")
        
        # Create a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == '__main__':
    start_server()
