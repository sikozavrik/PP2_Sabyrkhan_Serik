import re
t = input("Enter a string: ")
if re.fullmatch(r"a.*b", t):
    print("Match")
else:
    print("No match")