#Quotes and multiline strings
single_q = 'Hello'
double_q = "World"
multi_line = """Lorem ipsum dolor sit amet,
consectetur adipiscing elit."""
print(single_q, double_q)
print(multi_line)

#character access and string length
text = "Python"
print("First letter:", text[0])
print("String length:", len(text))

#String Slicing
phrase = "Hello, World!"
print("Chars from index 2 to 5:", phrase[2:5])
print("From start to index 5:", phrase[:5])
print("From index 7 to end:", phrase[7:])

#String Methods (upper, lower, strip, replace)
sample = "  Hello, Python!  "
print(sample.upper())
print(sample.lower())
print(sample.strip())  # Removes whitespace from ends
print(sample.replace("H", "J"))

#String Formatting (f-strings)
age = 20
txt = f"My name is Alex, and I am {age} years old."
print(txt)