from typing import BinaryIO
from constants import *
from request_handler import RequestHandler


class GetRequestHandler(RequestHandler):
    def __init__(self,
                 document_root: str,
                 connection,
                 uri: str,
                 http_version: str):
        self.connection = connection
        self._buffer_size = 1024
        super().__init__(document_root, connection, uri, http_version)

    def process(self):
        """
        This function is GET method handlers.
        Sends to client corresponding:
        - status line
        - headers
        - requested file
        """

        requested_file_path = self._get_requested_file_path()
        print(requested_file_path)

        try:
            with open(requested_file_path, 'rb') as f:
                self._respond_with_status_line(OK)
                self._respond_with_headers(file_path=requested_file_path,
                                           requested_headers=('Date',
                                                              'Content-Length',
                                                              'Content-Type',
                                                              'Server'))
                self._respond_with_file(f)
        except PermissionError:
            self._respond_with_status_line(FORBIDDEN)
            self._respond_with_headers(requested_headers=('Server',))
        except FileNotFoundError:
            self._respond_with_status_line(NOT_FOUND)
            self._respond_with_headers(requested_headers=('Server',))

    def _respond_with_file(self, file: BinaryIO):
        """
        This function sends requested file to client
        :param file: opened file descriptor
        :return:
        """
        while True:
            part = file.read(self._buffer_size)
            if not part:
                return
            self.connection.sendall(part)
