import socket
import time
import random
import string


# Server configuration
server_ip = "172.31.0.2"  # Replace with the server's IP address if not running locally(here replaced with alice1 IP)
server_port = 12000 #port number by which server application will be identified

# Number of pings to send. User can decide the number of pings to send
number_pings = int(input("Enter the number of pings: "))

# Initialize variables for RTT statistics
min_rtt = float('inf')
#initially taking all rtt's 0
max_rtt = 0
total_rtt = 0
packets_lost = 0

# Create a UDP socket with passing socket.SOCK_DGRAM in the second argument below
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#socket.SOCK_DGRAM is used for UDP
#socket.SOCK_STREAM is used for TCP

# Set a timeout for receiving responses (here we set it to 1 second as asked in the assignment)
client_socket.settimeout(1)

for sequence_number in range(1, number_pings + 1):
    # Generate a timestamp
    timestamp = time.time()

    # Generate a message with the sequence number and timestamp
    message = f"Ping {sequence_number} {timestamp}"

    # Record the start time
    start_time = time.time() #the moment we send the reqeust or message

    # Send the ping message to the server
    client_socket.sendto(message.encode('utf-8'), (server_ip, server_port))

    try:
        # Receive the response from the server
        data, server_address = client_socket.recvfrom(1024)

        # Record the end time
        end_time = time.time() #The moment we receive response from server

        # Calculate the RTT
        rtt = end_time - start_time

        # Update RTT statistics
        min_rtt = min(min_rtt, rtt)
        max_rtt = max(max_rtt, rtt)
        total_rtt += rtt

        # Print the response message, RTT, and timestamp
        print(f"Received response from {server_address}: {data.decode('utf-8')}, RTT = {rtt:.6f} seconds, Timestamp = {timestamp:.6f}")

    except socket.timeout:
        # If no response received within the timeout, print a timeout message
        packets_lost += 1
        print(f"Request timed out for sequence number {sequence_number}")

# Calculate and report statistics
average_rtt = total_rtt / number_pings
packet_loss_rate = (packets_lost / number_pings) * 100

print("\nPing statistics:")
print(f"Packets sent: {number_pings}")
print(f"Packets received: {number_pings - packets_lost}")
print(f"Packets lost: {packets_lost} ({packet_loss_rate:.2f}% loss)")
print(f"Minimum RTT: {min_rtt:.6f} seconds")
print(f"Maximum RTT: {max_rtt:.6f} seconds")
print(f"Average RTT: {average_rtt:.6f} seconds")

# Close the client socket
client_socket.close()
