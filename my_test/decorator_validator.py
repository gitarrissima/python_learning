
def validate_x_is_positive(func):

    def wrapper(*args, **kwargs):
        print("Validation in progress")
        print(args)
        if 'x' in kwargs and kwargs['x'] < 0:
            raise ValueError("x should be positive, but negative variable was received")
        func(*args, **kwargs)

    return wrapper


@validate_x_is_positive
def orig(x=5, y=3):
    print(x + y)


if __name__ == "__main__":
    orig(x=-1, y=2)
