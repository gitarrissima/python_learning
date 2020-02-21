import os
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
from mimetypes import MimeTypes
import socket


class HeaderGenerator:

    @staticmethod
    def get_date_header() -> str:
        now = datetime.now()
        stamp = mktime(now.timetuple())
        return f"Date: {format_date_time(stamp)}"

    @staticmethod
    def get_content_length_header(file_path: str) -> str:
        return f"Content-Length: {os.path.getsize(file_path)}"

    @staticmethod
    def get_content_type_header(file_path: str) -> str:
        mime = MimeTypes()
        return f"Content-Type: {mime.guess_type(file_path)[0]}"

    @staticmethod
    def get_server_header() -> str:
        return f"Server: {socket.gethostname()}"

    @staticmethod
    def get_connection_header() -> str:
        return f"Connection: keep-alive"
