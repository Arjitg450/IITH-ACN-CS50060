import socket
import sys
import re


def send_http_request(host, port, path):
    # Create a new socket for each request
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Construct and send the HTTP GET request
    request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
    client_socket.send(request.encode())

    # Receive and display the response
    response = b""
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        response += data

    client_socket.close()
    return response.decode()


def main():
    if len(sys.argv) < 4:
        print("Usage: python web_client.py <server_address> <server_port> <path>")
        sys.exit(1)

    server_address = sys.argv[1]
    server_port = int(sys.argv[2])
    path = sys.argv[3]

    response = send_http_request(server_address, server_port, path)

    # Display the response
    print(response)

    # Check for references to other objects in the HTML response
    if path.endswith(".html"):
        links = re.findall(r'href="(.*?)"', response)
        for link in links:
            print(f"Fetching: {link}")
            response = send_http_request(server_address, server_port, link)
            print(response)


if __name__ == "__main__":
    main()
