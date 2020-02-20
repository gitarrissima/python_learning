CRLF = b'\r\n'


class RequestParser:
    def __init__(self):
        self.request = b''
        self._request_line = b''

    @property
    def request_line(self):
        chunks = self._request_line.split()
        if len(chunks) != 3:
            raise ValueError(f"According to RFC request line should be this structure: "
                             f"'Method SP Request-URI SP HTTP-Version CRLF'. "
                             f"Check your data: {self._request_line}")

        return self._request_line

    @property
    def method(self):
        chunks = self.request_line.split()
        return chunks[0].upper().decode('utf-8')

    @property
    def uri(self):
        chunks = self.request_line.split()
        return chunks[1].decode('utf-8')

    @property
    def http_version(self):
        chunks = self.request_line.split()
        return chunks[-1].upper().decode('utf-8')

    @property
    def in_progress(self) -> bool:
        """
        This property identifies is HTTP request parsing done.

        :return:
        False if self._request_line is empty (not assembled)
        True if not
        """
        return self._request_line == b''

    def process_new_data(self, data: str):
        """
        This function assembles request and parses it according to HTTP proto structure.
        https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol#Request_message
        Note: In my realization I need request line only.

        :param data: new chunk of data collected from client
        """

        self.request += data
        if CRLF in self.request:
            chunks = self.request.split(CRLF)
            self._request_line = chunks[0]

