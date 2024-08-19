class C:
    def generator(self):
        for i in range(10):
            yield i

    def __iter__(self):
        return self.generator()


for i in C():
    print(i)

for i in C().generator():
    print(i)