import re
t = input("Enter a string: ")
if re.fullmatch(r"ab{2,3}", t):
    print("Match")
else:
    print("No match")