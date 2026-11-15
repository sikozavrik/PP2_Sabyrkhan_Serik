import re
t = input("Enter a string: ")
print(re.findall(r"[A-Z][a-z]+", t))