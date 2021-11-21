import socket
import sys
import inspect

# Define socket host and port
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8080

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print('Listening on port %s ...' % SERVER_PORT)

while True:
    # Wait for client connections
    client_connection, client_address = server_socket.accept()

    # Get the client request
    request = client_connection.recv(1024).decode()

    headers = request.split('\n')
    filename = headers[0].split()[1]

    # Get the content of the file
    # if filename == '/':
    #   filename = '/index.html'

    # print('./Web_File' + filename)
    filename = '/index.html'
    try:
        fin = open('./Web_File' + filename, encoding='utf-8')
        content = fin.read()
        fin.close()

        response = 'HTTP/1.0 200 OK\n\n' + content
    except FileNotFoundError:

        response = 'HTTP/1.0 404 NOT FOUND\n\nFile Not Found'

    # Send HTTP response
    client_connection.sendall(response.encode())
    client_connection.close()

# Close socket
server_socket.close()
