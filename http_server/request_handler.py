import sys
import os
from constants import *
from urllib.parse import unquote
from header_generator import HeaderGenerator


class RequestHandler:
    def __init__(self, document_root: str, connection, uri: str, http_version: str):
        self.uri = uri
        self.connection = connection
        self.http_version = http_version
        self.document_root = document_root
        self._header_generator = HeaderGenerator()

    def process(self):
        """
        This function is unsupported method handlers.
        Sends to client UNSUPPORTED response code
        """

        status_line = f"{self.http_version} {UNSUPPORTED} {DESCRIPTION[UNSUPPORTED]} {CRLF}{CRLF}"
        self.connection.sendall(status_line.encode('utf-8'))
        self._respond_with_headers()

    def _get_requested_file_path(self) -> str:
        """
        This function calculates full path of requested file:
        - changes uri path divider '/' to corresponding path divider according to os where server started
        - removes first '/' from path
        - performs url decode (unquote)
        - joins relative path with document_root
        - check if file is folder and specifies index.html as target file in case if requested entity is folder
        :return: requested full file path
        """
        relative_file_path = self._format_relative_path(self.uri)
        relative_file_path = unquote(relative_file_path)
        relative_file_path = relative_file_path.split('?')[0]
        requested_file_path = os.path.join(self.document_root, relative_file_path)

        if self.document_root not in os.path.abspath(requested_file_path):
            requested_file_path = self.document_root

        if os.path.isdir(requested_file_path):
            requested_file_path = os.path.join(requested_file_path, "index.html")

        return requested_file_path

    def _respond_with_status_line(self, type: str):
        """
        This function writes to client session starting line of requested type
        :param type: what kind of status
        :return:
        """
        status_line = f"{self.http_version} {type} {DESCRIPTION[type]}{CRLF}"
        self.connection.sendall(status_line.encode('utf-8'))

    def _respond_with_headers(self, file_path: str = None,
                              requested_headers: tuple = ('Date',
                                                          'Connection',
                                                          'Server')):
        """
        This function sends headers to client session
        :param file_path: we need to know file path to generate some headers
        :return:
        """
        headers = list()
        if 'Date' in requested_headers:
            headers.append(self._header_generator.get_date_header())
        if 'Content-Length' in requested_headers:
            headers.append(self._header_generator.get_content_length_header(file_path))
        if 'Content-Type' in requested_headers:
            headers.append(self._header_generator.get_content_type_header(file_path))
        if 'Server' in requested_headers:
            headers.append(self._header_generator.get_server_header())
        if 'Connection' in requested_headers:
            headers.append(self._header_generator.get_connection_header())

        end_of_headers = CRLF * 2
        headers_payload = (CRLF.join(headers) + end_of_headers).encode('utf-8')
        self.connection.sendall(headers_payload)

    @staticmethod
    def _format_relative_path(uri: str) -> str:
        """
        This function returns windows-like relative path from uri
        :param uri: for example /dir/filename.ext
        :return: string = dir\filename.txt
        """
        if 'win' in sys.platform:
            return uri[1:].replace('/', '\\')
        return uri[1:]
