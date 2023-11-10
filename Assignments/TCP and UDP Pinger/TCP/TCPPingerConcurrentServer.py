import socket
import threading
import random

# Server address and port
server_address = ('', 14000)  # Empty string in the address field means bind to all available interfaces

# Function to handle a client connection
def handle_client(client_socket, client_address):
    print(f'Connected to {client_address}')

    while True:
        data = client_socket.recv(1024)

        if not data:
            break  # No more data received, terminate connection

        # Generate a random number between 0 and 11 (both included)
        rand = random.randint(0, 11)

        if rand >= 4:
            # Capitalize the received data
            capitalized_data = data.upper()

            # Send the capitalized data back to the client
            client_socket.send(capitalized_data)
        else:
            # Packet is lost (no response)
            print(f'Packet lost (no response)')

    # Close the client socket
    client_socket.close()
    print(f'Connection with {client_address} closed')

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the server address and port
server_socket.bind(server_address)

# Listen for incoming connections (maximum 5 connections at a time)
server_socket.listen(5)

print('TCP Ping concurrent server is ready to receive connections...')

while True:
    # Wait for a client to connect
    client_socket, client_address = server_socket.accept()

    # Create a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
