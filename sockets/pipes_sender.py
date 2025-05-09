import win32pipe, win32file, pywintypes


def named_pipe_server():
    # Create a named pipe using the Windows API
    pipe_name = r'\\.\pipe\my_named_pipe'

    print("Creating named pipe...")
    try:
        # Create a pipe that can be used for communication
        pipe = win32pipe.CreateNamedPipe(
            pipe_name,  # Name of the pipe
            win32pipe.PIPE_ACCESS_OUTBOUND,  # Write-only access
            win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_WAIT,  # Message mode, blocking
            1,  # Max instances
            65536,  # Outbound buffer size
            65536,  # Inbound buffer size
            0,  # Default timeout
            None  # Security attributes
        )

        print("Waiting for client to connect...")
        # Wait for the client to connect
        win32pipe.ConnectNamedPipe(pipe, None)
        print("Client connected.")

        # Data to send through the pipe
        message = "Hello from the named pipe server!"

        # Write the message to the pipe
        win32file.WriteFile(pipe, message.encode('utf-8'))
        print("Message sent.")

        # Close the pipe after sending data
        win32file.CloseHandle(pipe)
    except pywintypes.error as e:
        print(f"Error: {e}")


# Run the named pipe server
named_pipe_server()
