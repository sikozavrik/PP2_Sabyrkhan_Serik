# sorted with key
students = [("Siko", 22), ("Temir", 19), ("Omir", 21)]
#by age
sorted_students = sorted(students, key=lambda x: x[1])
print(sorted_students)