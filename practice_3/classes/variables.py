# class variable vs instance variable

class Student:
    school = "High School"  
    def __init__(self, name):
        self.name = name

s1 = Student("Zhanboo")
s2 = Student("Siko")
print(s1.name, s1.school)
print(s2.name, s2.school)