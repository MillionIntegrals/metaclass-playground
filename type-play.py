class A:
    X = 5

    def f(self):
        print("Class A {}".format(self))


def f(self):
    print("Class B {}".format(self))

B = type("B", (), {'X': 6, 'f': f})


print(A)
print(B)

print(A.X)
print(B.X)

a = A()
b = B()

a.f()
b.f()




