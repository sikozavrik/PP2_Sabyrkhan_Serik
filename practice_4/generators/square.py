def f(n):
    for i in range(n + 1):
        yield i * i
n = int(input("Enter N: "))
for x in f(n):
    print(x)