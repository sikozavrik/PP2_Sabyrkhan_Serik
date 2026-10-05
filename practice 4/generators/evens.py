def f(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield i
n = int(input("Enter a number: "))
r = []
for x in f(n):
    r.append(str(x))
print(",".join(r))