import functools
import itertools


def disable():
    """
    Disable a decorator by re-assigning the decorator's name
    to this function. For example, to turn off memoization:

    >>> memo = disable

    """
    return


def decorator(func):
    """ 
    Decorate a decorator so that it inherits the docstrings
    and stuff from the function it's decorating.
    """ 

    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper_decorator


def countcalls(func):
    """Decorator that counts calls made to the function decorated."""

    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        wrapper_decorator.calls += 1
        print(f'Function \'{func.__name__}\' was called {wrapper_decorator.calls} times')
        return func(*args, **kwargs)

    wrapper_decorator.calls = 0
    return wrapper_decorator


def memo(func):
    """
    Memoize a function so that it caches all return values for
    faster future lookups.
    """

    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        cache_key = args + tuple(kwargs.items())
        if cache_key not in wrapper_decorator.cache:
            wrapper_decorator.cache[cache_key] = func(*args, **kwargs)
        return wrapper_decorator.cache[cache_key]

    wrapper_decorator.cache = dict()
    return wrapper_decorator


def n_ary(func):
    """
    Given binary function f(x, y), return an n_ary function such
    that f(x, y, z) = f(x, f(y,z)), etc. Also allow f(x) = x.
    """

    @functools.wraps(func)
    def wrapper_decorator(*args):
        it = itertools.accumulate(args, func)
        last = next(it)
        for last in it:
            pass
        return last
    return wrapper_decorator


def trace(formatter: str = '____'):
    """Trace calls made to function decorated.

    @trace("____")
    def fib(n):
        ....

    >>> fib(3)
     --> fib(3)
    ____ --> fib(2)
    ________ --> fib(1)
    ________ <-- fib(1) == 1
    ________ --> fib(0)
    ________ <-- fib(0) == 1
    ____ <-- fib(2) == 2
    ____ --> fib(1)
    ____ <-- fib(1) == 1
     <-- fib(3) == 3

    """
    def decorator_trace(func):

        @functools.wraps(func)
        def wrapper_decorator(*args):

            mul = wrapper_decorator.level
            mul_formatter = formatter * mul
            print(f'{mul_formatter} --> {func.__name__}({args[0]})')
            wrapper_decorator.level += 1
            value = func(*args)
            wrapper_decorator.level -= 1
            print(f'{mul_formatter} --> {func.__name__}({args[0]}) = {value}')
            return value

        wrapper_decorator.level = 0
        return wrapper_decorator

    return decorator_trace


@memo
@countcalls
@n_ary
def foo(a, b):
    return a + b


@countcalls
@memo
@n_ary
def bar(a, b):
    return a * b


@countcalls
@trace("####")
@memo
def fib(n):
    """Some doc"""
    return 1 if n <= 1 else fib(n-1) + fib(n-2)


def main():
    print(foo(4, 3))
    print(foo(4, 3, 2))
    print(foo(4, 3))
    print("foo was called", foo.calls, "times")

    print(bar(4, 3))
    print(bar(4, 3, 2))
    print(bar(4, 3, 2, 1))
    print("bar was called", bar.calls, "times")

    print(fib.__doc__)
    fib(3)
    print(fib.calls, 'calls made')


if __name__ == '__main__':
    main()
