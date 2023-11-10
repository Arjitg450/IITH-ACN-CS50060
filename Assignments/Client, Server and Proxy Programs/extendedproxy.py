import socket
import threading
from queue import Queue
import requests
from bs4 import BeautifulSoup

HOST = "127.0.0.2"
PORT = 12347

# Create a dictionary to store cached web pages with full HTML content
html_cache = {}

def get_cached_page(url):
    return html_cache.get(url, None)

def cache_page(url, html_content):
    html_cache[url] = html_content

def fetch_web_page(url):
    cached_page = get_cached_page(url)
    if cached_page:
        return cached_page

    # If not cached, fetch the page from the web
    response = requests.get(url)
    if response.status_code == 200:
        content = response.text

        # Cache the page for future use
        cache_page(url, content)
        return content
    else:
        return None

def extract_links_and_cache(html_content, base_url):
    soup = BeautifulSoup(html_content, 'html.parser')
    threads = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith('http'):
            link_url = href
        else:
            link_url = f'{base_url}/{href}' if not href.startswith('/') else f'{base_url}{href}'
        
        # Add error handling to avoid invalid URLs
        try:
            thread = threading.Thread(target=cache_linked_page, args=(link_url,))
            threads.append(thread)
            thread.start()
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch and cache {link_url}: {e}")
    
    for thread in threads:
        thread.join()

def cache_linked_page(url):
    linked_page_content = fetch_web_page(url)
    if linked_page_content:
        cache_page(url, linked_page_content)

def handle_server(path, server_add, server_port, queue):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((server_add, server_port))
    print(f"[CONNECTED] Connected to the server on ('{server_add},{server_port}')")

    request = f"GET {path} HTTP/1.1\r\nHost: {server_add}\r\nConnection: close\r\n\r\n"
    server_socket.send(request.encode())

    response = b""
    while True:
        data = server_socket.recv(1024)
        if not data:
            break
        response += data

    server_socket.close()
    queue.put(response)

def handle_client(client_socket):
    request_data = client_socket.recv(1024).decode()
    request_lines = request_data.split("\n")
    request_line = request_lines[0]
    method, path, _ = request_line.split()
    request_line = request_lines[1]
#     _, server_add = request_line.split()
#     request_line = request_lines[2]
#     _, server_port = request_line.split()
#     server_port = int(server_port)

    server_add = '192.168.135.246'
    server_port = 15200

    # Check if the requested web page is already cached
    cached_page = get_cached_page(f'http://{server_add}:{server_port}{path}')
    
    if cached_page:
        client_socket.send(cached_page.encode())
    else:
        result_queue = Queue()
        server_thread = threading.Thread(target=handle_server, args=(path, server_add, server_port, result_queue))
        server_thread.start()
        server_thread.join()
        response = result_queue.get()
        
        # Extract links and cache linked pages
        extract_links_and_cache(response, f'http://{server_add}:{server_port}{path}')
        
        client_socket.send(response)

    client_socket.close()

def start_proxy_server():
    proxy_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_server_socket.bind((HOST, PORT))
    proxy_server_socket.listen(5)
    print(f"[LISTENING] Web Proxy Server is listening on {HOST}:{PORT}")

    while True:
        client_socket, client_address = proxy_server_socket.accept()
        print(f"[CONNECTED] Accepted connection from {client_address}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    start_proxy_server()
