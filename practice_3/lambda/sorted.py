# sorted with key
students = [("Alex", 22), ("Kate", 19), ("John", 21)]
#by age
sorted_students = sorted(students, key=lambda x: x[1])
print(sorted_students)