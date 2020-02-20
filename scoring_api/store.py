import redis

MAX_RETRIES = 3


def with_retries(max_retries: int = MAX_RETRIES):
    def retry(func):
        def wrapped(*args, **kwargs):

            last_exception = None
            for _ in range(max_retries):
                print(f"try# {_}")
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e

            return last_exception
        return wrapped
    return retry


class Store:

    def __init__(self, host: str = 'localhost', port: int = 6379) -> None:
        self.host = host
        self.port = port
        self.timeout = 30
        self.redis = self._get_connection()
        self.max_retries = 3

    def _get_connection(self):
        return redis.Redis(host=self.host, port=self.port, db=0)

    @with_retries()
    def get(self, key: str):
        return self.redis.get(key)

    @with_retries()
    def cache_get(self, key: str):
        return self.redis.get(key)

    @with_retries()
    def cache_set(self, key: str, value: str):
        return self.redis.set(key, value)


