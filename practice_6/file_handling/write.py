import string

with open("sample.txt", "w") as f:
    f.write("Line 1\nLine 2\n")

with open("sample.txt", "a") as f:
    f.write("Line 3\n")

fruits = ["Apple", "Banana", "Cherry"]
with open("fruits.txt", "w") as f:
    for fruit in fruits:
        f.write(fruit + "\n")

for letter in string.ascii_uppercase:
    with open(f"{letter}.txt", "w") as f:
        f.write(f"File {letter}\n")