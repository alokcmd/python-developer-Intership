
# Week 2: Core Concepts and Skills
# Python Developer Internship

# 1. Variables and Data Types
name = "Alok"
age = 21
language = "Python"

print("Name:", name)
print("Age:", age)
print("Programming Language:", language)

# 2. Conditional Statements
marks = 85

if marks >= 80:
    print("Grade: A")
elif marks >= 60:
    print("Grade: B")
else:
    print("Grade: C")

# 3. Loops
print("\nNumbers from 1 to 5:")

for number in range(1, 6):
    print(number)

# 4. Functions
def add_numbers(a, b):
    return a + b

result = add_numbers(10, 20)
print("\nSum:", result)

# 5. List Operations
numbers = [10, 20, 30, 40, 50]

print("List:", numbers)
print("First Element:", numbers[0])
print("Total Elements:", len(numbers))

# 6. Dictionary
student = {
    "name": "Alok",
    "course": "BTech CSE",
    "skill": "Python"
}

print("\nStudent Details:")

for key, value in student.items():
    print(key, ":", value)

# 7. Object-Oriented Programming
class Student:
    def __init__(self, student_name):
        self.student_name = student_name

    def display(self):
        print("Student Name:", self.student_name)

student1 = Student("Alok")
student1.display()

print("\nWeek 2 Python practice completed!")
