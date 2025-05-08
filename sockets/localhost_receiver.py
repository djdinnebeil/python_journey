import socket

def local_client():
    # Create a TCP/IP socket for connecting to the local server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the local server on localhost:65432
    client_socket.connect(('127.0.0.1', 65432))

    # Receive the message from the server
    message = client_socket.recv(1024).decode('utf-8')
    print("Received from server:", message)

    # Close the connection
    client_socket.close()

# Run the client function
local_client()
