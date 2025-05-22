from app.cores.singleton import SingletonMeta


def test_singleton_meta():
    class MyClass(metaclass=SingletonMeta):
        def __init__(self, value):
            self.value = value

    instance1 = MyClass("first")
    instance2 = MyClass("second")

    # Both instance1 and instance2 should be the same object
    assert instance1 is instance2
    # Value remains "first" since the second call won't create a new object
    assert instance1.value == "first"
    assert instance2.value == "first"
