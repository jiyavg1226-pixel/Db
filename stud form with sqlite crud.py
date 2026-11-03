import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# =================================
# 1. DATABASE CONNECTION
# =================================

conn = sqlite3.connect("student.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    phone TEXT,
    course TEXT
)
""")

conn.commit()


# =================================
# 2. MAIN WINDOW
# =================================

root = Tk()
root.title("Student Registration Form")
root.geometry("700x600")
root.configure(bg="ivory")


# =================================
# 3. HEADING
# =================================

Label(root, text="STUDENT REGISTRATION FORM",
      font=("Arial", 20, "bold"),
      bg="ivory", fg="darkblue").pack(pady=15)


# =================================
# 4. INPUT FIELDS
# =================================

Label(root, text="Name:",
      bg="ivory").pack()

name_entry = Entry(root, width=35)
name_entry.pack(pady=5)


Label(root, text="Email:",
      bg="ivory").pack()

email_entry = Entry(root, width=35)
email_entry.pack(pady=5)


Label(root, text="Phone:",
      bg="ivory").pack()

phone_entry = Entry(root, width=35)
phone_entry.pack(pady=5)


Label(root, text="Course:",
      bg="ivory").pack()

course_entry = Entry(root, width=35)
course_entry.pack(pady=5)


# =================================
# 5. CREATE OPERATION (INSERT)
# =================================

def insert_data():

    name = name_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()
    course = course_entry.get()

    if name == "" or email == "" or phone == "" or course == "":
        messagebox.showwarning("Warning", "Please fill all fields!")
        return

    cursor.execute("""
    INSERT INTO students (name, email, phone, course)
    VALUES (?, ?, ?, ?)
    """, (name, email, phone, course))

    conn.commit()

    messagebox.showinfo("Success", "Student Added Successfully!")

    clear_fields()
    display_data()


# =================================
# 6. READ OPERATION (DISPLAY)
# =================================

def display_data():

    for row in tree.get_children():
        tree.delete(row)

    cursor.execute("SELECT * FROM students")

    for row in cursor.fetchall():
        tree.insert("", END, values=row)


# =================================
# 7. SELECT RECORD
# =================================

def select_record(event):

    selected = tree.focus()

    if selected:
        data = tree.item(selected, "values")

        clear_fields()

        name_entry.insert(0, data[1])
        email_entry.insert(0, data[2])
        phone_entry.insert(0, data[3])
        course_entry.insert(0, data[4])


# =================================
# 8. UPDATE OPERATION
# =================================

def update_data():

    selected = tree.focus()

    if not selected:
        messagebox.showwarning("Warning", "Select a Student!")
        return

    data = tree.item(selected, "values")
    student_id = data[0]

    cursor.execute("""
    UPDATE students
    SET name=?, email=?, phone=?, course=?
    WHERE id=?
    """, (
        name_entry.get(),
        email_entry.get(),
        phone_entry.get(),
        course_entry.get(),
        student_id
    ))

    conn.commit()

    messagebox.showinfo("Success", "Student Updated Successfully!")

    clear_fields()
    display_data()


# =================================
# 9. DELETE OPERATION
# =================================

def delete_data():

    selected = tree.focus()

    if not selected:
        messagebox.showwarning("Warning", "Select a Student!")
        return

    data = tree.item(selected, "values")
    student_id = data[0]

    answer = messagebox.askyesno(
        "Confirm",
        "Do you want to delete this student?"
    )

    if answer:

        cursor.execute(
            "DELETE FROM students WHERE id=?",
            (student_id,)
        )

        conn.commit()

        messagebox.showinfo("Success", "Student Deleted Successfully!")

        clear_fields()
        display_data()


# =================================
# 10. CLEAR FUNCTION
# =================================

def clear_fields():

    name_entry.delete(0, END)
    email_entry.delete(0, END)
    phone_entry.delete(0, END)
    course_entry.delete(0, END)


# =================================
# 11. BUTTONS
# =================================

Button(root, text="INSERT",
       command=insert_data,
       bg="green", fg="white",
       width=12).pack(pady=5)

Button(root, text="UPDATE",
       command=update_data,
       bg="blue", fg="white",
       width=12).pack(pady=5)

Button(root, text="DELETE",
       command=delete_data,
       bg="red", fg="white",
       width=12).pack(pady=5)

Button(root, text="CLEAR",
       command=clear_fields,
       bg="orange", fg="black",
       width=12).pack(pady=5)


# =================================
# 12. DISPLAY TABLE
# =================================

tree = ttk.Treeview(
    root,
    columns=("ID", "Name", "Email", "Phone", "Course"),
    show="headings"
)

tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Email", text="Email")
tree.heading("Phone", text="Phone")
tree.heading("Course", text="Course")

tree.pack(pady=15, fill=BOTH, expand=True)

tree.bind("<<TreeviewSelect>>", select_record)


# Display Existing Records
display_data()


# =================================
# 13. RUN APPLICATION
# =================================

root.mainloop()

conn.close()
