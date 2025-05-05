import sqlite3

def connect_db():
    return sqlite3.connect('students.db')

def create_table():
    with connect_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER,
                grade TEXT
            )
        ''')

def add_student(name, age, grade):
    with connect_db() as conn:
        conn.execute('INSERT INTO students (name, age, grade) VALUES (?, ?, ?)', (name, age, grade))
        print("Student added.")

def view_students():
    with connect_db() as conn:
        cursor = conn.execute('SELECT * FROM students')
        for row in cursor.fetchall():
            print(row)

def update_student(student_id, name, age, grade):
    with connect_db() as conn:
        cursor = conn.execute('SELECT * FROM students WHERE id = ?', (student_id,))
        student = cursor.fetchone()
        if student:
            conn.execute(
                'UPDATE students SET name = ?, age = ?, grade = ? WHERE id = ?',
                (name, age, grade, student_id)
            )
            print(f"Student with ID {student_id} updated.")
        else:
            print(f"No student found with ID {student_id}.")

def delete_student(student_id):
    with connect_db() as conn:
        cursor = conn.execute('SELECT * FROM students WHERE id = ?', (student_id,))
        student = cursor.fetchone()
        if student:
            conn.execute('DELETE FROM students WHERE id = ?', (student_id,))
            print(f"Student with ID {student_id} deleted.")
        else:
            print(f"No student found with ID {student_id}.")

def search_student(name):
    with connect_db() as conn:
        cursor = conn.execute('SELECT * FROM students WHERE name LIKE ?', ('%' + name + '%',))
        results = cursor.fetchall()
        if results:
            for row in results:
                print(row)
        else:
            print(f"No student found with name matching '{name}'.")

def menu():
    create_table()
    while True:
        print("\n--- Student Manager ---")
        print("1. Add student")
        print("2. View students")
        print("3. Update student")
        print("4. Delete student")
        print("5. Search by name")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            name = input("Name: ")
            try:
                age = int(input("Age: "))
            except ValueError:
                print("Age must be a number.")
                continue
            grade = input("Grade: ")
            add_student(name, age, grade)

        elif choice == '2':
            view_students()

        elif choice == '3':
            try:
                student_id = int(input("Student ID to update: "))
                with connect_db() as conn:
                    cursor = conn.execute('SELECT * FROM students WHERE id = ?', (student_id,))
                    student = cursor.fetchone()
                    if not student:
                        print(f"No student found with ID {student_id}.")
                        continue
                    print(f"Current: ID={student[0]}, Name={student[1]}, Age={student[2]}, Grade={student[3]}")
                    name = input("New name: ")
                    age = int(input("New age: "))
                    grade = input("New grade: ")
                    update_student(student_id, name, age, grade)
            except ValueError:
                print("Invalid input.")

        elif choice == '4':
            try:
                student_id = int(input("Student ID to delete: "))
                delete_student(student_id)
            except ValueError:
                print("Invalid ID.")

        elif choice == '5':
            name = input("Enter name to search: ")
            search_student(name)

        elif choice == '6':
            print("Exiting Student Manager.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    menu()
