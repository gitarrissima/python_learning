import os
from constants import *
from request_handler import RequestHandler


class HeadRequestHandler(RequestHandler):
    def __init__(self, document_root: str, connection, uri: bytes, http_version: str):
        super().__init__(document_root, connection, uri, http_version)

    def process(self):
        """
        This function is HEAD method handlers.
        Sends to client corresponding:
        - status line
        - headers
        """

        requested_file_path = self._get_requested_file_path()

        if os.path.exists(requested_file_path):
            self._respond_with_status_line(OK)
            self._respond_with_headers(file_path=requested_file_path,
                                       requested_headers=('Date',
                                                          'Content-Length',
                                                          'Content-Type',
                                                          'Server'))
        else:
            self._respond_with_status_line(NOT_FOUND)
            self._respond_with_headers(requested_headers=('Server',))
