import re
t = input("Enter a string: ")
if re.fullmatch(r"ab*", t):
    print("Match")
else:
    print("No match")