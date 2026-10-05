import re
t = input("Enter a string: ")
print(re.sub(r"([A-Z])", r" \1", t).strip())