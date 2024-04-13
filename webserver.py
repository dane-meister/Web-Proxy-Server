import socket
import os
import sys
# Import necessary libraries,
# socket for networking, os to interact with the file system, sys for system-specific parameters and functions

# The port on which the server will listen
SERVER_PORT = 6789
# The buffer size for receiving data from the web server
BUFFER_SIZE = 1024
# The maximum number of connections the proxy server can handle
MAX_CONNECTIONS = 5


def start_server():
    # Create a socket object using socket.AF_INET for IPv4 and socket.SOCK_STREAM for TCP
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except socket.error as e:
        print(f"Failed to create socket: {e}")
        sys.exit(1)

    try:
        # Bind the socket to a specific IP address and port
        server_socket.bind(('', SERVER_PORT))
    except socket.error as e:
        print(f"Failed to bind socket: {e}")
        sys.exit(1)

    try:
        # Put the socket into server mode to listen for incoming connections
        server_socket.listen(MAX_CONNECTIONS)
    except socket.error as e:
        print(f"Failed to listen on socket: {e}")
        sys.exit(1)

    print(f"Server is ready to receive on port {SERVER_PORT}")

    try:
        while True:
            # Accept a connection from a client
            connection_socket, address = server_socket.accept()
            try:
                # Receive the request message from the client
                message = connection_socket.recv(BUFFER_SIZE).decode()
                # Extract the path of the requested object from the message
                file_name = message.split()[1]
                file_path = file_name[1:]  # Remove the leading '/'
                print(f"File path: {file_path}")
                if os.path.exists(file_path) and os.path.isfile(file_path):
                    print(f"File {file_path} exists")
                    with open(file_path, 'rb') as file:
                        # Read the file and store the contents in output_data
                        output_data = file.read()
                        # Create the HTTP response header line based on the requested file
                        if file_path.endswith(('.jpg', '.jpeg', '.png')):
                            mime_type = 'image/jpeg' if file_path.endswith(('.jpg', '.jpeg')) else 'image/png'
                        else:
                            mime_type = 'text/html'  # Default MIME type
                        # Create the HTTP response header
                        header = f'HTTP/1.1 200 OK\r\nContent-Type: {mime_type}\r\nContent-Length: {len(output_data)}' \
                                 f'\r\n\r\n'
                        # Send the HTTP response header line to the connection socket
                        connection_socket.send(header.encode())
                        # Send the content of the requested file to the connection socket
                        connection_socket.send(output_data)
                else:
                    # Send response message for file not found
                    header = 'HTTP/1.1 404 Not Found\n\n'
                    output_data = b'<html><body><h1>404 Not Found</h1></body></html>'
                    connection_socket.sendall(header.encode() + output_data)

            except IOError:
                # Send response message for file not found
                header = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n'
                output_data = '<html><body><h1>404 Not Found</h1></body></html>'
                connection_socket.sendall((header + output_data).encode())
            except IndexError:
                # Ignore requests that do not contain a file path
                pass
            finally:
                # Close the client connection socket
                connection_socket.close()
    except KeyboardInterrupt:
        # Close the server socket
        print("\nServer is shutting down...")
        try:
            # Attempt to close the server socket
            server_socket.close()
            print("Server successfully shut down.")
        except Exception as e:
            print(f"Error occurred when shutting down the server: {e}")
        finally:
            sys.exit(0)


def main():
    start_server()


if __name__ == "__main__":
    main()
