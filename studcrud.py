from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

# Database Connection
con = sqlite3.connect("student.db")
cur = con.cursor()

# Create Student Table
cur.execute("""
CREATE TABLE IF NOT EXISTS student (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    email TEXT NOT NULL,
    course TEXT NOT NULL
)
""")
con.commit()

selected_id = None

# Main Window
root = Tk()
root.title("Student Registration Form")
root.geometry("850x550")
root.configure(bg="lightblue")


# Clear All Fields
def clear_fields():
    global selected_id
    selected_id = None

    name_entry.delete(0, END)
    age_entry.delete(0, END)
    email_entry.delete(0, END)
    course_entry.delete(0, END)


# Read / Display Student Data
def read_data():
    for row in tree.get_children():
        tree.delete(row)

    cur.execute("SELECT * FROM student")
    rows = cur.fetchall()

    for row in rows:
        tree.insert("", END, values=row)


# Create Student
def create_data():
    name = name_entry.get()
    age = age_entry.get()
    email = email_entry.get()
    course = course_entry.get()

    if name == "" or age == "" or email == "" or course == "":
        messagebox.showwarning("Warning", "Please fill all fields")
        return

    if not age.isdigit() or int(age) <= 0:
        messagebox.showwarning("Warning", "Enter a valid age")
        return

    cur.execute(
        "INSERT INTO student (name, age, email, course) VALUES (?, ?, ?, ?)",
        (name, int(age), email, course)
    )

    con.commit()

    messagebox.showinfo("Success", "Student Added Successfully")

    clear_fields()
    read_data()


# Select Student
def select_data(event):
    global selected_id

    selected = tree.focus()

    if selected == "":
        return

    values = tree.item(selected, "values")

    # Clear entries without resetting selected_id
    name_entry.delete(0, END)
    age_entry.delete(0, END)
    email_entry.delete(0, END)
    course_entry.delete(0, END)

    selected_id = values[0]

    name_entry.insert(0, values[1])
    age_entry.insert(0, values[2])
    email_entry.insert(0, values[3])
    course_entry.insert(0, values[4])


# Update Student
def update_data():
    if selected_id is None:
        messagebox.showwarning("Warning", "Please select a student")
        return

    name = name_entry.get()
    age = age_entry.get()
    email = email_entry.get()
    course = course_entry.get()

    if name == "" or age == "" or email == "" or course == "":
        messagebox.showwarning("Warning", "Please fill all fields")
        return

    if not age.isdigit() or int(age) <= 0:
        messagebox.showwarning("Warning", "Enter a valid age")
        return

    cur.execute("""
        UPDATE student
        SET name=?, age=?, email=?, course=?
        WHERE id=?
    """, (name, int(age), email, course, selected_id))

    con.commit()

    messagebox.showinfo("Success", "Student Updated Successfully")

    clear_fields()
    read_data()


# Delete Student
def delete_data():
    if selected_id is None:
        messagebox.showwarning("Warning", "Please select a student")
        return

    answer = messagebox.askyesno(
        "Confirm",
        "Are you sure you want to delete?"
    )

    if answer:
        cur.execute("DELETE FROM student WHERE id=?", (selected_id,))
        con.commit()

        messagebox.showinfo("Success", "Student Deleted Successfully")

        clear_fields()
        read_data()


# Heading
title = Label(
    root,
    text="STUDENT REGISTRATION FORM",
    font=("Arial", 20, "bold"),
    bg="lightblue",
    fg="darkblue"
)
title.pack(pady=15)


# Form Frame
form_frame = Frame(root, bg="lightblue")
form_frame.pack(pady=10)


# Student Name
Label(form_frame, text="Student Name:", font=("Arial", 12),
      bg="lightblue").grid(row=0, column=0, padx=10, pady=8)

name_entry = Entry(form_frame, font=("Arial", 12), width=25)
name_entry.grid(row=0, column=1, padx=10, pady=8)


# Age
Label(form_frame, text="Age:", font=("Arial", 12),
      bg="lightblue").grid(row=1, column=0, padx=10, pady=8)

age_entry = Entry(form_frame, font=("Arial", 12), width=25)
age_entry.grid(row=1, column=1, padx=10, pady=8)


# Email
Label(form_frame, text="Email:", font=("Arial", 12),
      bg="lightblue").grid(row=2, column=0, padx=10, pady=8)

email_entry = Entry(form_frame, font=("Arial", 12), width=25)
email_entry.grid(row=2, column=1, padx=10, pady=8)


# Course
Label(form_frame, text="Course:", font=("Arial", 12),
      bg="lightblue").grid(row=3, column=0, padx=10, pady=8)

course_entry = Entry(form_frame, font=("Arial", 12), width=25)
course_entry.grid(row=3, column=1, padx=10, pady=8)


# Buttons
button_frame = Frame(root, bg="lightblue")
button_frame.pack(pady=10)

Button(button_frame, text="CREATE", width=12,
       command=create_data).grid(row=0, column=0, padx=5)

Button(button_frame, text="READ", width=12,
       command=read_data).grid(row=0, column=1, padx=5)

Button(button_frame, text="UPDATE", width=12,
       command=update_data).grid(row=0, column=2, padx=5)

Button(button_frame, text="DELETE", width=12,
       command=delete_data).grid(row=0, column=3, padx=5)

Button(button_frame, text="CLEAR", width=12,
       command=clear_fields).grid(row=0, column=4, padx=5)


# Student Table
tree = ttk.Treeview(
    root,
    columns=("ID", "Name", "Age", "Email", "Course"),
    show="headings"
)

tree.heading("ID", text="ID")
tree.heading("Name", text="Student Name")
tree.heading("Age", text="Age")
tree.heading("Email", text="Email")
tree.heading("Course", text="Course")

tree.column("ID", width=50)
tree.column("Name", width=150)
tree.column("Age", width=70)
tree.column("Email", width=200)
tree.column("Course", width=150)

tree.pack(pady=15, fill=X, padx=20)

# Select Row Event
tree.bind("<<TreeviewSelect>>", select_data)

# Display Existing Records
read_data()

# Close Database Properly
def close_app():
    con.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", close_app)

# Run Application
root.mainloop()
