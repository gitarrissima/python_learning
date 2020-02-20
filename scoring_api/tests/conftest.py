import pytest
import threading
import os
import sys
from http.server import HTTPServer
from mock import MagicMock
from functools import partial

cur_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(cur_dir + '\\..')
sys.path.append(cur_dir)
import api
from store import Store


def get_store_magic_mock():
    store_magic_mock = MagicMock(Store)
    store_magic_mock.get.return_value = []
    store_magic_mock.cache_get.return_value = 0.5
    store_magic_mock.cache_set.return_value = 0.5
    return store_magic_mock


@pytest.fixture(scope="module")
def end_to_end_setup():
    store = get_store_magic_mock()
    handler = partial(api.MainHTTPHandler, store)
    server = HTTPServer(("localhost", 8001), handler)
    thread = threading.Thread(target=server.serve_forever)
    try:
        thread.daemon = True
        thread.start()
        yield
    except Exception:
        pass


@pytest.fixture(scope="module")
def api_connection():
    class Requester:
        def __init__(self):
            self.context = {}
            self.headers = {}
            self.store = get_store_magic_mock()

        def get_response(self, request):
            return api.method_handler({"body": request, "headers": self.headers}, self.context, self.store)

    return Requester()

