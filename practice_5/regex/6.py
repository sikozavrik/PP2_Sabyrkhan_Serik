import re
t = input("Enter a string: ")
print(re.sub(r"[ ,.]", ":", t))