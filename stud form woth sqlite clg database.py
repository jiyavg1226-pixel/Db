import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# DATABASE CONNECTION

conn = sqlite3.connect("clg.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS stud1 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll_no TEXT,
    name TEXT,
    department TEXT,
    course TEXT,
    semester TEXT
)
""")

conn.commit()

# MAIN WINDOW

root = Tk()
root.title("College Student Registration")
root.geometry("850x650")
root.configure(bg="ivory")

# HEADING

Label(root, text="COLLEGE STUDENT REGISTRATION",
      font=("Arial", 20, "bold"),
      bg="ivory", fg="darkblue").pack(pady=15)

# INPUT FIELDS

frame = Frame(root, bg="ivory")
frame.pack(pady=10)

Label(frame, text="Roll Number:",
      bg="ivory").grid(row=0, column=0, padx=10, pady=8)

roll = Entry(frame, width=30)
roll.grid(row=0, column=1)

Label(frame, text="Student Name:",
      bg="ivory").grid(row=1, column=0, padx=10, pady=8)

name = Entry(frame, width=30)
name.grid(row=1, column=1)

Label(frame, text="Department:",
      bg="ivory").grid(row=2, column=0, padx=10, pady=8)

department = ttk.Combobox(
    frame, width=27,
    values=["Computer Science", "IT", "Commerce", "Management"]
)
department.grid(row=2, column=1)

Label(frame, text="Course:",
      bg="ivory").grid(row=3, column=0, padx=10, pady=8)

course = ttk.Combobox(
    frame, width=27,
    values=["BCA", "BBA", "BSC", "MCA"]
)
course.grid(row=3, column=1)

Label(frame, text="Semester:",
      bg="ivory").grid(row=4, column=0, padx=10, pady=8)

semester = ttk.Combobox(
    frame, width=27,
    values=["1", "2", "3", "4", "5", "6"]
)
semester.grid(row=4, column=1)


# CLEAR FUNCTION

def clear():
    roll.delete(0, END)
    name.delete(0, END)
    department.set("")
    course.set("")
    semester.set("")


# INSERT DATA

def insert_data():

    if (roll.get() == "" or name.get() == "" or
        department.get() == "" or course.get() == "" or
        semester.get() == ""):

        messagebox.showwarning("Warning", "Fill all fields!")
        return

    cursor.execute("""
        INSERT INTO stud1
        (roll_no, name, department, course, semester)
        VALUES (?, ?, ?, ?, ?)
    """, (
        roll.get(), name.get(), department.get(),
        course.get(), semester.get()
    ))

    conn.commit()

    messagebox.showinfo("Success", "Student Registered Successfully!")

    clear()
    display_data()


# DISPLAY DATA

def display_data():

    for row in tree.get_children():
        tree.delete(row)

    cursor.execute("SELECT * FROM stud1")

    for row in cursor.fetchall():
        tree.insert("", END, values=row)


# SELECT STUDENT

def select_student(event):

    selected = tree.focus()

    if selected:
        data = tree.item(selected, "values")

        clear()

        roll.insert(0, data[1])
        name.insert(0, data[2])
        department.set(data[3])
        course.set(data[4])
        semester.set(data[5])


# UPDATE DATA

def update_data():

    selected = tree.focus()

    if not selected:
        messagebox.showwarning("Warning", "Select Student!")
        return

    data = tree.item(selected, "values")
    student_id = data[0]

    cursor.execute("""
        UPDATE stud1
        SET roll_no=?, name=?,
            department=?, course=?, semester=?
        WHERE id=?
    """, (
        roll.get(), name.get(), department.get(),
        course.get(), semester.get(), student_id
    ))

    conn.commit()

    messagebox.showinfo("Success", "Student Updated Successfully!")

    clear()
    display_data()


# DELETE DATA

def delete_data():

    selected = tree.focus()

    if not selected:
        messagebox.showwarning("Warning", "Select Student!")
        return

    data = tree.item(selected, "values")

    answer = messagebox.askyesno(
        "Confirm", "Delete Student Record?"
    )

    if answer:
        cursor.execute(
            "DELETE FROM stud1 WHERE id=?",
            (data[0],)
        )

        conn.commit()

        messagebox.showinfo("Success", "Student Deleted Successfully!")

        clear()
        display_data()


# BUTTONS

button_frame = Frame(root, bg="ivory")
button_frame.pack(pady=10)

Button(button_frame, text="INSERT",
       command=insert_data,
       bg="green", fg="white",
       width=12).grid(row=0, column=0, padx=5)

Button(button_frame, text="UPDATE",
       command=update_data,
       bg="blue", fg="white",
       width=12).grid(row=0, column=1, padx=5)

Button(button_frame, text="DELETE",
       command=delete_data,
       bg="red", fg="white",
       width=12).grid(row=0, column=2, padx=5)

Button(button_frame, text="CLEAR",
       command=clear,
       bg="orange", fg="black",
       width=12).grid(row=0, column=3, padx=5)


# STUDENT TABLE

columns = (
    "ID", "Roll", "Name",
    "Department", "Course", "Semester"
)

tree = ttk.Treeview(
    root, columns=columns,
    show="headings", height=8
)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)

tree.pack(pady=15, fill=BOTH, expand=True)

tree.bind("<<TreeviewSelect>>", select_student)

# DISPLAY EXISTING RECORDS

display_data()

# RUN APPLICATION

root.mainloop()

conn.close()

