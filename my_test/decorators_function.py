def modifier(func):
    def wrapper(*args, **kwargs):
        print('wrapper')
        func(*args, **kwargs)
    print('modifier')
    return wrapper


@modifier
def original(a):
    print('original')
    print(a)


RETRIES_LIMIT = 3


def with_retries(retries_limit=RETRIES_LIMIT):

    def retry(func):
        def wrapped(*args, **kwargs):
            last_raised = None
            for _ in range(retries_limit):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_raised = e
                    print(f"{str(e)}")
            return last_raised

        return wrapped

    return retry


@with_retries(retries_limit=2)
def zero_division(n):
    print(f"Trying 5/0")
    return n/0


class WithRetry:
    def __init__(self, retries_limit=RETRIES_LIMIT):
        print(f"WithRetry __init__")
        self.retries_limit = retries_limit

    def __call__(self, func):
        print(f"WithRetry __call__")

        def wrapped(*args, **kwargs):
            print(f"WithRetry __call__ wrapped")
            last_raised = None
            for _ in range(self.retries_limit):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_raised = e
                    print(f"{str(e)}")
            return last_raised
        return wrapped


@WithRetry(retries_limit=2)
def gen_exception(input_str: str):
    return input_str + 2.3


if __name__ == '__main__':
    # test = modifier(original)
    # print(test)
    # test(3)

    # original(3)

    # zero_division(5)
    gen_exception("test")

