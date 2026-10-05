import re
t = input("Enter a string: ")
print(re.findall(r"[a-z]+(?:_[a-z]+)+", t))