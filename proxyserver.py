import socket
import os
import hashlib
import json

# Configuration:
# The host on which the server will listen
SERVER_HOST = 'localhost'
# The port on which the server will listen
SERVER_PORT = 6677
# The address of the proxy server
SERVER_ADDRESS = (SERVER_HOST, SERVER_PORT)
# The buffer size for receiving data from the web server
BUFFER_SIZE = 1024
# The maximum number of connections the proxy server can handle
MAX_CONNECTIONS = 5
# Cache file
CASH_FILE_PATH = "./cache.json"


def modify_cached_response_headers(cached_response):
    # Convert the cached response to a string to manipulate headers
    response_str = cached_response.decode('iso-8859-1')
    
    # Split the response into headers and body
    headers, body = response_str.split('\r\n\r\n', 1)
    header_lines = headers.split('\r\n')
    
    # Modify the Cache-Control header to make the response public and cacheable for 1 hour
    has_cache_control = False
    for i, line in enumerate(header_lines):
        if line.startswith('Cache-Control:'):
            header_lines[i] = 'Cache-Control: public, max-age=3600'
            has_cache_control = True
            break
    if not has_cache_control:
        header_lines.append('Cache-Control: public, max-age=3600')
    
    # Reassemble the response
    modified_response = '\r\n'.join(header_lines) + '\r\n\r\n' + body
    return modified_response.encode('iso-8859-1')


def get_cache_key(url):
    # Generate a hash for the URL to use as a key
    return hashlib.md5(url.encode('utf-8')).hexdigest()


def is_cached(cache, url):
    # Check if the URL response is cached
    cache_key = get_cache_key(url)
    return cache_key in cache


def save_to_cache(cache, url, data):
    # Save the response data to the cache file
    cache_key = get_cache_key(url)
    cache[cache_key] = data.decode('iso-8859-1')  # Assuming the data is text


def read_from_cache(cache, url):
    # Read the cached response data
    cache_key = get_cache_key(url)
    return cache[cache_key].encode('iso-8859-1')  # Re-encode the data to bytes using 'iso-8859-1' encoding


def write_cache(cache):
    # Write the cache to the file
    with open(CASH_FILE_PATH, 'w') as cache_file:
        json.dump(cache, cache_file)


 # Load cache
def load_cache():
    # Load the cache from the cache file
    try:
        with open(CASH_FILE_PATH, 'r') as cache_file:
            return json.load(cache_file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def handle_client_request(client_connection):
    try:
        # Receive the request from the client
        request = client_connection.recv(BUFFER_SIZE).decode()
        print(f"Received request: {request}")
        # Extract the URL from the request
        lines = request.split('\n')
        method, url, _ = lines[0].split(' ')
        # Return the method and URL
        return method, url
    except ValueError as e:
        # Handle the ValueError gracefully
        print(f"ValueError occurred: {e}")
        return None, None


def extract_domain_and_path(url):
    # Normalize the URL by removing the protocol (http:// or https://)
    if url.startswith('http://'):
        normalized_url = url[len('http://'):]
    elif url.startswith('https://'):
        normalized_url = url[len('https://'):]
    else:
        normalized_url = url

    # Find the end of the domain part
    domain_end = normalized_url.find('/')
    if domain_end == -1:
        # No slash found, entire URL is the domain, and path is assumed to be '/'
        domain = normalized_url
        path = '/'
    else:
        # Split the URL into domain and path
        domain = normalized_url[:domain_end]
        path = normalized_url[domain_end:]
    # Return the domain and path
    return domain, path


def fetch_from_server(url):
    try:
        # Extract domain and path from URL
        domain, path = extract_domain_and_path(url[1:])
        print(f"Domain: {domain}, Path: {path}")
        # Create a new socket to connect to the web server
        web_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to the web server
        web_socket.connect((domain, 80))
        # Create the request to send to the web server
        fwd_request = f"GET {path} HTTP/1.0\r\nHost: {domain}\r\n\r\n"
        print(f"request: {fwd_request}")
        # Send the request to the web server
        web_socket.sendall(fwd_request.encode())
        response = b""
        while True:
            # Receive the response from the web server
            part = web_socket.recv(1024)
            if not part:
                break
            response += part
        # Close the connection to the web server
        web_socket.close()
        # Return the response
        return response
    except Exception as e:
        # Return a 404 error if the request fails
        print(f"Error fetching from server: {e}")
        return b"HTTP/1.0 404 Not Found\r\n\r\n"


def main():
    # Initialize cache file
    if not os.path.exists(CASH_FILE_PATH):
        with open(CASH_FILE_PATH, 'w') as cache_file:
            json.dump({}, cache_file)

    # Create TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(SERVER_ADDRESS)
    server_socket.listen(MAX_CONNECTIONS)

    print(f"Proxy Server running on {SERVER_HOST}:{SERVER_PORT}")

    # Proxy server loop
    try:
        while True:
            # Accept client connection
            client_connection, _ = server_socket.accept()
            method, url = handle_client_request(client_connection)
            # Load cache
            cache = load_cache()

            # Check if URL is cached
            if method == 'GET' and is_cached(cache, url):
                print("Serving from cache")
                # Read the response from the cache
                cached_response = read_from_cache(cache, url)
                # Modify the response headers
                response = modify_cached_response_headers(cached_response)
            elif method == 'GET':
                print("Fetching from server")
                # Fetch the response from the web server
                response = fetch_from_server(url)
                # Save the response to the cache
                save_to_cache(cache, url, response)
                # Write the cache to the file
                write_cache(cache)
            else:
                response = b"HTTP/1.0 405 Method Not Allowed\r\n\r\n"

            # Send the response to the client
            client_connection.sendall(response)
            client_connection.close()
            
    except KeyboardInterrupt:
        # Close the server socket
        print("Shutting down the server.")
        server_socket.close()


if __name__ == "__main__":
    main()