t = input("Enter snake case: ")
w = t.split("_")
r = w[0]
for x in w[1:]:
    r = r + x.capitalize()
print(r)