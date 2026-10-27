
import json
import os

FILE_NAME = "students.json"


def load_students():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            print("Warning: Could not read saved records.")
    return []


def save_students(students):
    with open(FILE_NAME, "w") as file:
        json.dump(students, file, indent=4)


def add_student(students):
    name = input("Enter student name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    roll = input("Enter roll number: ").strip()
    if not roll:
        print("Roll number cannot be empty.")
        return

    if any(s["roll"] == roll for s in students):
        print("This roll number already exists.")
        return

    try:
        marks = float(input("Enter marks (0-100): "))
        if not 0 <= marks <= 100:
            print("Marks must be between 0 and 100.")
            return
    except ValueError:
        print("Please enter valid numeric marks.")
        return

    students.append({
        "name": name,
        "roll": roll,
        "marks": marks
    })
    save_students(students)
    print("Student added successfully!")


def view_students(students):
    if not students:
        print("No student records found.")
        return

    for student in students:
        print(
            f"Name: {student['name']} | "
            f"Roll: {student['roll']} | "
            f"Marks: {student['marks']}"
        )


def search_student(students):
    roll = input("Enter roll number to search: ").strip()

    for student in students:
        if student["roll"] == roll:
            print("Student found:", student)
            return

    print("Student not found.")


def main():
    students = load_students()

    while True:
        print("\n--- Student Management System ---")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_student(students)
        elif choice == "2":
            view_students(students)
        elif choice == "3":
            search_student(students)
        elif choice == "4":
            print("Thank you for using the system!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
