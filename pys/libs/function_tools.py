import functools


def main(something, another='item') -> bool:
    if another == 'item':
        return True


func0 = functools.partial(main, 'test', 'another test')
func1 = functools.partial(main, 'test')

print(func0(), func1())
