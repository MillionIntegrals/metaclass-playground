class SingletonBase:
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls, *args, **kwargs)

        return cls.instance


class A(SingletonBase):
    pass


class B(A):
    pass


print(A())
print(A())
print(B())

