import win32file, win32pipe, pywintypes


def named_pipe_client():
    # The same pipe name used by the server
    pipe_name = r'\\.\pipe\my_named_pipe'

    print("Connecting to named pipe...")
    try:
        # Connect to the named pipe created by the server
        handle = win32file.CreateFile(
            pipe_name,  # Pipe name
            win32file.GENERIC_READ,  # Read-only access
            0,  # No sharing
            None,  # Default security
            win32file.OPEN_EXISTING,  # Open existing pipe
            0,  # Default attributes
            None  # No template file
        )

        print("Successfully connected to the server.")

        # Read from the named pipe
        result, data = win32file.ReadFile(handle, 65536)  # Read up to 64 KB
        print("Received from server:", data.decode('utf-8'))

        # Close the handle after reading
        win32file.CloseHandle(handle)
    except pywintypes.error as e:
        print(f"Error: {e}")


# Run the named pipe client
named_pipe_client()
