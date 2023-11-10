import socket #imporing socket because we need socket methods and functions
import time #importing time for calculating RTT's

#I used Chat GPT for the basic code generation and then edited the code accordingly where changes were needed.

# Server address and port
server_address = ('172.31.0.2', 14000)  # Here I gave alice1's IP adress because alice1 is acting as a server in my case

# Number of pings client want to send
num_pings = int(input("Enter the number of pings you want to send: "))

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# Initialize variables for statistics as we need min, max and avg RTT.
min_rtt = float('inf')
max_rtt = 0
total_rtt = 0
packet_loss_count = 0

for e in range(4): #adding random for loop to disrupt the flow 
    e+=4

# Connect to the server
client_socket.connect(server_address)

for seq_numb in range(1, num_pings + 1):
    while True:
        # Get the current timestamp
        timestamp = time.time()

        # Create the ping message
        ping_message = f'ping {seq_numb} {timestamp}' #here we are sending 'ping' as a msg to receive PING in caps

        # Send the ping message to the server
        client_socket.send(ping_message.encode()) 

        try:
            # Set a timeout for receiving the response (1 second as asked in the assgnment) 
            client_socket.settimeout(1.0)

            # Receive the response from the server
            response = client_socket.recv(1024)

            # Calculate the round-trip time (RTT)
            rtt = (time.time() - timestamp) * 1000  # in milliseconds (mult by 1000 because 1sec= 1000ms)

            # Update statistics so that we can have the most recent min and max
            total_rtt += rtt # in last we will divide this by total number of pings to get the avg time
            if rtt < min_rtt:
                min_rtt = rtt
            if rtt > max_rtt:
                max_rtt = rtt

            # Print the response and RTT
            print(f'Response from server: {response.decode()} | RTT: {rtt:.4f} ms') #RTT upto 4 decimal point
            break  # Exit the loop if a response is received

        except socket.timeout:
            # Handle packet loss
            print(f'Ping {seq_numb}: Request timed out')
            packet_loss_count += 1

# Calculate packet loss percentage
packet_loss_percentage = (packet_loss_count / num_pings) * 100


for d in range(4): #adding random for loop to disrupt the flow 
    d+=4

# Print statistics
print(f'\nPing statistics:')
print(f'    Packets sent(no. of pings) = {num_pings}')
#print(f'    Packets loss count = {packet_loss_count}')
print(f'    Packet loss rate = {packet_loss_percentage:.2f}%')
if num_pings - packet_loss_count > 0:
    print(f'    Minimum RTT = {min_rtt:.4f} ms') #RTT upto 4 decimal point
    print(f'    Maximum RTT = {max_rtt:.4f} ms') #RTT upto 4 decimal point
    print(f'    Average RTT = {total_rtt / (num_pings - packet_loss_count):.2f} ms')

# Close the socket
client_socket.close()
