Web Proxy Server

This project includes a simple web server and a proxy server implemented in Python using socket programming. The web server is designed to handle one HTTP request at a time, serving files from the server's file system and returning appropriate HTTP responses. The proxy server caches web pages and serves requests either from the cache or by fetching content from the web server, improving performance by reducing the need to fetch the same content multiple times.

## External Libraries Used
No external libraries were used in this project beyond those that come with a standard Python installation. The project relies on the socket, os, sys, hashlib, and json libraries for its functionality.

### socket
- Purpose: The socket module in Python provides access to the BSD socket interface. It is used for handling network connections. In the given code, this module is crucial for creating socket objects, both for the web server and the proxy server, enabling them to listen for incoming connections on specified ports, accept connections, and send and receive data over the network.

### os
- Purpose: The os module in Python provides a way of using operating system dependent functionality. In the context of the web server, it is used to interact with the file system, particularly to check if a requested file exists (os.path.exists) and whether it is a file (os.path.isfile).

### sys
- Purpose: The sys module provides access to some variables used or maintained by the Python interpreter and to functions that interact strongly with the interpreter. In the server code, sys.exit() is used to terminate the Python program when an exception occurs during the socket creation, binding, or listening process.

### hashlib
- Only in Proxy Server; Purpose: The hashlib module is used to perform cryptographic hashing. In the proxy server, it's used to generate a hash value for URLs. This hash value serves as a unique key for each URL to store and retrieve cached responses in a file, ensuring that each cached content is uniquely identified.

### json
- Only in Proxy Server; Purpose: The json module provides an easy way to encode and decode data in JSON format. It is used in the proxy server to read and write the cache data to and from a file (cache.json). JSON is chosen for its simplicity and ease of use in storing structured data, making it ideal for caching web content.

These libraries are part of the Python Standard Library, which means they are available in any standard Python installation and do not require external packages to be installed. They provide the necessary functionalities to implement network communication, file handling, data encoding, and cryptographic operations, which are essential for building the web and proxy servers as described.

## Instructions on How to Run the Programs

### Web Server

1. Place an HTML file (e.g., HelloWorld.html) in the same directory as the web server script (webserver.py).

2. Run the web server script:
python webserver.py

3. Determine the IP address of the host running the server, or use localhost if running on the same machine.

4. Open a web browser and navigate to the URL corresponding to your setup, e.g., http://localhost:6789/HelloWorld.html, replacing localhost with your IP address if necessary.

### Proxy Server

1. Run the proxy server script:
python proxyserver.py

2. Configure your web browser to use the proxy server by setting the proxy to localhost and the port to 6677, or to the IP address and port of your proxy server if running on a different machine.

3. Navigate to a web page through your browser configured to use the proxy, e.g., http://localhost:6677/http://www.google.com.

### Working Webpages

The web server and proxy server have been tested and respectively work successfully for fetching and caching content from the following webpages:

- http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file2.html
- http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file3.html
- http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file4.html
- http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file5.html
- http://www.google.com 


Please ensure that the web server is running before attempting to access these pages through the proxy server.

This project is a part of an academic assignment and is used for educational purposes only.
