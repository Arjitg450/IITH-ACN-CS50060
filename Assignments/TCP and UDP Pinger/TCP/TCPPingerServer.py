import socket
import random #imporing random for incuring random loss of packets

# Server address and port
server_address = ('', 14000)  # Empty string in the address field means bind to all available interfaces

# Create a TCP socket, here we used socket.SOCK_STREAM for TCP connection
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the server address and port
server_socket.bind(server_address)

# Listen for incoming connections (maximum 1 connection at a time for simplicity)
server_socket.listen(1)

print('TCP Ping server is ready to receive connection from Client(Bob1)...')

while True:
    # Wait for a client to connect
    client_socket, client_address = server_socket.accept()

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
