import socket   # Import the socket library for network communication
import pickle   # Import pickle for deserializing the received data

def start_client():
    # Define the server's IP address and port number to connect to
    server_address = ('localhost', 65432)

    # Create a TCP/IP socket for connecting to the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Connect to the server using the address
        client_socket.connect(server_address)

        # Receive the first 4 bytes which represent the length of the incoming data
        data_length = int.from_bytes(client_socket.recv(4), 'big')

        # Prepare an empty binary string to collect the data
        binary_data = b''

        # Loop to read the data in chunks until the full message is received
        while len(binary_data) < data_length:
            # Receive data in chunks of 1024 bytes
            packet = client_socket.recv(1024)
            # Break the loop if no more data is received
            if not packet:
                break
            # Append the received packet to the binary data
            binary_data += packet

        # Deserialize the received binary string back into a Python object
        received_data = pickle.loads(binary_data)

        # Print the deserialized data
        print("Received Data:", received_data)

# Start the client function
start_client()
