class Salut:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.d = 3

    def count(self):
        self.c = self.a + self.b
        return self.c

print(Salut.count(1, 3))