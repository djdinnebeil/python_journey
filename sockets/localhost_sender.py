import socket

def local_server():
    # Create a TCP/IP socket for local communication
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind to localhost (127.0.0.1) and an arbitrary port (65432)
    server_socket.bind(('127.0.0.1', 65432))

    # Listen for a single incoming connection
    server_socket.listen(1)
    print("Server listening on localhost:65432")

    # Accept a connection from a client
    conn, addr = server_socket.accept()
    with conn:
        print(f"Connected by {addr}")

        # Send a message to the client
        message = "Hello from the server!"
        conn.sendall(message.encode('utf-8'))
        print("Message sent to client")

# Run the server function
local_server()
