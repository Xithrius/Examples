class Test:

    def __init__(self, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs

    def test_func(self) -> None:
        self.args = 'Nothing'


class Test2(Test):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


obj0 = Test(0, test=1)
obj1 = Test2(0, test=3)

print(obj0.args, obj0.kwargs)
print(obj1.args, obj1.kwargs)

obj0.test_func()
obj1.test_func()

print(obj0.args, obj0.kwargs)
print(obj1.args, obj1.kwargs)
