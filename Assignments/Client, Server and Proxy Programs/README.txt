# Simple Python HTTP Server and Web Proxy

This project consists of three Python scripts that demonstrate primary HTTP client and server functionality along with a simple web proxy server. Each script is described below.

## 1. `client.py`

This script acts as a basic HTTP client and allows you to send HTTP GET requests to a specified server and path. It can also parse HTML responses for links and fetch them.

### Modules
1. HTTP GET request to server the server
2. Module Name: send_http_request_server

   2.1his module uses the Server address and port number to send a GET request
3. Module Name: send_http_request_to_proxy

   3.1 This module uses the Web Proxy Server address and port number to send a GET request to the Web Proxy Server 

### Usage

To use the `client.py` script, run it from the command line with the following arguments:
```bash
# This is a bash command to run client.py
>>> python3 client.py
```

- `<server_address>`: The IP address or domain of the server you want to send the request to.
- `<server_port>`: The port on which the server is listening.
- `<path>`: The path to the resource you want to request.

## 2. `server.py`

This script implements a basic HTTP server that can serve static files from the server's directory. It listens on a specified IP address and port.

### Usage

To use the `server.py` script, simply run it from the command line. The server will listen on the specified IP address and port. You can access files in the server's directory by making HTTP GET requests.
To use the `Server.py` script, run it from the command line with the following arguments:
```bash
# This is a bash command to run client.py
>>> python3 Server.py
```
## 3. `Proxy`

This script acts as a simple web proxy server that forwards HTTP requests to a specified server and returns the responses to clients. It can be used to intercept and inspect traffic between clients and web servers.

### Usage

To use the `web proxy server.py` script, run it from the command line. The proxy server listens on the specified IP address and port. Clients should configure their browsers or applications to use this proxy server. The proxy server will forward client requests to the destination server and return the responses to clients.
To use the `ExtendedProxy.py` script, run it from the command line with the following arguments:
```bash
# This is a bash command to run client.py
>>> python3 Proxy.py
```

## Dependencies

All scripts in this project rely on Python's standard library and do not require any additional packages or modules.
