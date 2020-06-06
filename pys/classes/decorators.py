import functools
import typing as t


def outer(func: t.Callable) -> t.Callable:

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> t.Any:
        res = func(*args, **kwargs)

        return res

    return wrapper


class Deco:

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, func):
        print(self.kwargs.get('name'))

        def execute(*args, **kwargs):
            return func(*args, **kwargs)

        return execute


@Deco(name='the add function')
def add(num1, num2):
    return num1 + num2


print(add(3, 4))
