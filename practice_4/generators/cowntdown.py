def f(n):
    for i in range(n, -1, -1):
        yield i
n = int(input("Enter a number: "))
for x in f(n):
    print(x)