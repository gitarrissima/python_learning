import sys
import socket
import signal
import threading
from request_parser import RequestParser
from get_request_handler import GetRequestHandler
from head_request_handler import HeadRequestHandler
from request_handler import RequestHandler


class HTTPServer:
    def __init__(self,
                 host: str = 'localhost',
                 port: int = 80,
                 document_root: str = 'C:\\Users\\Sakharova\\Documents\\Learning\PythonProjects\\python_learning\\http_server\\tests'):
        self.host = host
        self.port = port
        self.document_root = document_root

    def threaded(self, connection):
        with connection:
            request_parser = RequestParser()
            while request_parser.in_progress:
                request_parser.process_new_data(connection.recv(1024))

            print(f"Data received {request_parser.request_line}")

            method = request_parser.method
            uri = request_parser.uri
            http_version = request_parser.http_version

            if method == 'GET':
                request_handler = GetRequestHandler(self.document_root, connection, uri, http_version)
            elif method == 'HEAD':
                request_handler = HeadRequestHandler(self.document_root, connection, uri, http_version)
            else:
                request_handler = RequestHandler(self.document_root, connection, uri, http_version)

            request_handler.process()

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen(5)
            while True:
                conn, address = s.accept()
                thread = threading.Thread(target=self.threaded, args=[conn])
                thread.start()


if __name__ == '__main__':
    server = HTTPServer()
    server.start()
