#Checking data types using type()
x_str = "Hello World"
x_int = 20
x_float = 20.5
print(type(x_str))
print(type(x_int))
print(type(x_float))

#ssequence types (List, Tuple, Range)
my_list = ["apple", "banana", "cherry"]  # list
my_tuple = ("apple", "banana", "cherry") # tuple
my_range = range(6)                      # range
print(type(my_list), type(my_tuple), type(my_range))

#Mapping and Set types (Dict, Set)
my_dict = {"name": "John", "age": 36}    # dict
my_set = {"apple", "banana", "cherry"}   # set
print(type(my_dict), type(my_set))

# Boolean type
is_active = True
is_valid = False
print(type(is_active))
print(is_active, is_valid)

#None and Binary types
empty_val = None                         # NoneType
raw_bytes = b"Hello"                     # bytes
print(type(empty_val))
print(type(raw_bytes))