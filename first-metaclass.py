class Meta(type):
    def __init__(cls, name, bases, namespace):
        super(Meta, cls).__init__(name, bases, namespace)
        print("Creating new class: {}".format(cls))

    def __call__(cls):
        new_instance = super(Meta, cls).__call__()
        print("Class {} new instance: {}".format(cls, new_instance))
        return new_instance


class C(metaclass=Meta):
    pass

c = C()

print(c)
