import socket

# Server address and port
server_address = ('', 12000)  # Empty string in the address field means bind to all available interfaces

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the server address and port
server_socket.bind(server_address)

# Listen for incoming connections (maximum 1 connection at a time for simplicity)
server_socket.listen(1)

print('TCP Ping server is ready to receive connections...')

while True:
    # Wait for a client to connect
    client_socket, client_address = server_socket.accept()

    print(f'Connected to {client_address}')

    while True:
        data = client_socket.recv(1024)

        if not data:
            break  # No more data received, terminate connection

        # Capitalize the received message
        response = data.upper()

        # Send the response back to the client
        client_socket.send(response)

    # Close the client socket
    client_socket.close()
