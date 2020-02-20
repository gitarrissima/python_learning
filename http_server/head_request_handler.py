from constants import *
from request_handler import RequestHandler


class HeadRequestHandler(RequestHandler):
    def __init__(self, document_root: str, connection, uri: bytes, http_version: str):
        super().__init__(document_root, connection, uri, http_version)

    def process(self):
        """
        This function is HEAD method handlers.
        Sends to client corresponding response code and requested file
        """

        requested_file_path = self._get_requested_file_path()

        try:
            with open(requested_file_path, 'rb'):
                self._respond_with_status_line(OK)
                self._respond_with_headers(requested_file_path)
        except PermissionError:
            self._respond_with_status_line(FORBIDDEN)
        except FileNotFoundError:
            self._respond_with_status_line(NOT_FOUND)
            self._respond_with_headers(requested_headers=('Server',))

