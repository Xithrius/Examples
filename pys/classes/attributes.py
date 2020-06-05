class Something:

    def __init__(self, *args, **kwargs) -> None:
        self.test = 1

    def func(self, new_test: int = None) -> None:
        if new_test:
            self.test = new_test


obj = Something()
print(obj.test)

obj.test = 2
print(obj.test)

obj.func()
print(obj.test)

obj.func(3)
print(obj.test)
