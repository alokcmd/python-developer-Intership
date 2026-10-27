
from flask import Flask, request, redirect, url_for, render_template_string
import sqlite3

app = Flask(__name__)
DATABASE = "students.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_number TEXT NOT NULL UNIQUE,
            course TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Student Management System</title>
    <style>
        body { font-family: Arial; margin: 40px; background: #f3f4f6; }
        .container { max-width: 850px; margin: auto; background: white;
                     padding: 25px; border-radius: 10px; }
        input { padding: 10px; margin: 5px; }
        button { padding: 10px 15px; cursor: pointer; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { padding: 10px; border: 1px solid #ddd; text-align: left; }
        th { background: #e5e7eb; }
        a { margin-right: 8px; }
    </style>
</head>
<body>
<div class="container">
    <h1>Student Management System</h1>

    <h3>Add Student</h3>
    <form action="{{ url_for('add_student') }}" method="POST">
        <input name="name" placeholder="Student Name" required>
        <input name="roll_number" placeholder="Roll Number" required>
        <input name="course" placeholder="Course" required>
        <button type="submit">Add Student</button>
    </form>

    {% if message %}
        <p>{{ message }}</p>
    {% endif %}

    <h3>Student Records</h3>
    <table>
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Roll Number</th>
            <th>Course</th>
            <th>Actions</th>
        </tr>
        {% for student in students %}
        <tr>
            <td>{{ student['id'] }}</td>
            <td>{{ student['name'] }}</td>
            <td>{{ student['roll_number'] }}</td>
            <td>{{ student['course'] }}</td>
            <td>
                <a href="{{ url_for('edit_student', student_id=student['id']) }}">Edit</a>
                <form action="{{ url_for('delete_student', student_id=student['id']) }}"
                      method="POST" style="display:inline">
                    <button type="submit"
                            onclick="return confirm('Delete this student?')">
                        Delete
                    </button>
                </form>
            </td>
        </tr>
        {% endfor %}
    </table>
</div>
</body>
</html>
"""


EDIT_HTML = """
<!DOCTYPE html>
<html>
<head><title>Edit Student</title></head>
<body style="font-family:Arial; margin:40px">
    <h2>Edit Student</h2>
    <form method="POST">
        <p>Name: <input name="name" value="{{ student['name'] }}" required></p>
        <p>Roll Number:
           <input name="roll_number" value="{{ student['roll_number'] }}" required>
        </p>
        <p>Course: <input name="course" value="{{ student['course'] }}" required></p>
        <button type="submit">Save Changes</button>
    </form>
    <p><a href="{{ url_for('home') }}">Back to Home</a></p>
</body>
</html>
"""


@app.route("/")
def home():
    conn = get_db_connection()
    students = conn.execute(
        "SELECT * FROM students ORDER BY id DESC"
    ).fetchall()
    conn.close()

    message = request.args.get("message", "")
    return render_template_string(HTML, students=students, message=message)


@app.route("/add", methods=["POST"])
def add_student():
    name = request.form["name"].strip()
    roll_number = request.form["roll_number"].strip()
    course = request.form["course"].strip()

    if not name or not roll_number or not course:
        return redirect(url_for("home", message="All fields are required."))

    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO students (name, roll_number, course) VALUES (?, ?, ?)",
            (name, roll_number, course)
        )
        conn.commit()
        message = "Student added successfully."
    except sqlite3.IntegrityError:
        message = "This roll number already exists."
    finally:
        conn.close()

    return redirect(url_for("home", message=message))


@app.route("/edit/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    conn = get_db_connection()
    student = conn.execute(
        "SELECT * FROM students WHERE id = ?", (student_id,)
    ).fetchone()

    if student is None:
        conn.close()
        return "Student not found", 404

    if request.method == "POST":
        name = request.form["name"].strip()
        roll_number = request.form["roll_number"].strip()
        course = request.form["course"].strip()

        if not name or not roll_number or not course:
            conn.close()
            return "All fields are required.", 400

        try:
            conn.execute(
                """UPDATE students
                   SET name = ?, roll_number = ?, course = ?
                   WHERE id = ?""",
                (name, roll_number, course, student_id)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return "That roll number is already used by another student.", 400

        conn.close()
        return redirect(url_for("home", message="Student updated successfully."))

    conn.close()
    return render_template_string(EDIT_HTML, student=student)


@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("home", message="Student deleted."))


@app.route("/health")
def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    create_table()
    app.run(debug=True)
