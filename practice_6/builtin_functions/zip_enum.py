names = ["Alice", "Bob", "Charlie"]
scores = [85, 92, 78]

for index, name in enumerate(names, start=1):
    print(index, name)

for name, score in zip(names, scores):
    print(name, score)

value = "123"
print("Type of value:", type(value))
print("Is string:", isinstance(value, str))

num = int(value)
print("Converted to int:", num, type(num))