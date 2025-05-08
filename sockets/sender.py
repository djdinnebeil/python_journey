import socket  # Import the socket library for network communication
import pickle  # Import pickle for serializing Python objects


def start_server():
    # Define the server's IP address and port number as a tuple
    server_address = ('localhost', 65432)

    # Create a TCP/IP socket using IPv4 addressing (AF_INET) and TCP (SOCK_STREAM)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Bind the socket to the address and port
        server_socket.bind(server_address)

        # Listen for incoming connections (1 client at a time)
        server_socket.listen()
        print("Server listening on:", server_address)

        # Accept a connection from a client
        connection, client_address = server_socket.accept()

        # Once a connection is established, use the connection in a context
        with connection:
            print("Connected by:", client_address)

            # Create a dictionary to send to the client
            data = {'message': 'Hello, Client!', 'status': 'success', 'code': 200}

            # Serialize the dictionary into a binary string using pickle
            binary_data = pickle.dumps(data)

            # Send the length of the serialized data as a 4-byte integer
            # This ensures the client knows how much data to expect
            connection.send(len(binary_data).to_bytes(4, 'big'))

            # Send the actual serialized binary data
            connection.sendall(binary_data)
            print("Data sent to client.")


# Start the server function
start_server()
