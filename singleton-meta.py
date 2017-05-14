class SingletonMeta(type):
    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        cls.instance = None

    def __call__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__call__(*args, **kwargs)

        return cls.instance


class SingletonBaseMeta(metaclass=SingletonMeta):
    pass


class A(SingletonBaseMeta):
    pass


class B(A):
    pass


print(A())
print(A())
print(B())
