class X:
    def a(self):
        return ['a', 'b']

class X1(X):
    def a(self):
        return super().a()

    def b(self):
        x = super().a()
        x.append('c')
        return x

x1 = X1()
print(x1.a())
print(x1.b())

