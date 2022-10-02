import socket
import threading
import traceback
import app


def listening(client_conn):
    # non persistent http
    try:
        client_request = client_conn.recv(1024).decode('utf-8')
        # print(client_request)
        # * fot testing
        response = app.HTTP_request_handler(client_request)
        # already byte string
        client_conn.sendall(response)
    except:
        traceback.print_exc()
    finally:
        client_conn.close()


class Server:
    def __init__(self, host='140.115.200.237', port: int = 8080):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        print('Listening on port %s ...' % port)

    def start_listen(self):
        while True:
            client_conn, client_addr = self.server_socket.accept()
            threading.Thread(target=listening, args=(client_conn,)).start()
