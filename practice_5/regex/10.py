import re
t = input("Enter camel case: ")
r = re.sub(r"([A-Z])", r"_\1", t).lower()
if r.startswith("_"):
    r = r[1:]
print(r)