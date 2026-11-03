from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

# Database Connection
con = sqlite3.connect("employee1.db")
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS employee (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    salary REAL NOT NULL,
    phone TEXT NOT NULL
)
""")
con.commit()

root = Tk()
root.title("Employee Details - CRUD Operations")
root.geometry("850x550")
root.config(bg="lightblue")

selected_id = None


# Clear Form
def clear_fields():
    global selected_id
    selected_id = None

    name_entry.delete(0, END)
    dept_entry.delete(0, END)
    salary_entry.delete(0, END)
    phone_entry.delete(0, END)

    tree.selection_remove(tree.selection())


# READ Operation
def read_data():
    for item in tree.get_children():
        tree.delete(item)

    cur.execute("SELECT * FROM employee")

    for row in cur.fetchall():
        tree.insert("", END, values=row)


# CREATE Operation
def create_data():
    name = name_entry.get().strip()
    department = dept_entry.get().strip()
    salary = salary_entry.get().strip()
    phone = phone_entry.get().strip()

    if not name or not department or not salary or not phone:
        messagebox.showwarning("Warning", "Please fill all fields")
        return

    try:
        salary_value = float(salary)

        if salary_value < 0:
            raise ValueError

    except ValueError:
        messagebox.showerror("Error", "Please enter a valid salary")
        return

    cur.execute("""
        INSERT INTO employee (name, department, salary, phone)
        VALUES (?, ?, ?, ?)
    """, (name, department, salary_value, phone))

    con.commit()
    read_data()
    clear_fields()

    messagebox.showinfo("Success", "Employee Added Successfully")


# Select Employee from Table
def select_data(event):
    global selected_id

    selected = tree.focus()

    if selected:
        values = tree.item(selected, "values")
        selected_id = values[0]

        name_entry.delete(0, END)
        dept_entry.delete(0, END)
        salary_entry.delete(0, END)
        phone_entry.delete(0, END)

        name_entry.insert(0, values[1])
        dept_entry.insert(0, values[2])
        salary_entry.insert(0, values[3])
        phone_entry.insert(0, values[4])


# UPDATE Operation
def update_data():
    if selected_id is None:
        messagebox.showwarning("Warning", "Please select an employee first")
        return

    name = name_entry.get().strip()
    department = dept_entry.get().strip()
    salary = salary_entry.get().strip()
    phone = phone_entry.get().strip()

    if not name or not department or not salary or not phone:
        messagebox.showwarning("Warning", "Please fill all fields")
        return

    try:
        salary_value = float(salary)

        if salary_value < 0:
            raise ValueError

    except ValueError:
        messagebox.showerror("Error", "Please enter a valid salary")
        return

    cur.execute("""
        UPDATE employee
        SET name=?, department=?, salary=?, phone=?
        WHERE id=?
    """, (name, department, salary_value, phone, selected_id))

    con.commit()
    read_data()
    clear_fields()

    messagebox.showinfo("Success", "Employee Updated Successfully")


# DELETE Operation
def delete_data():
    if selected_id is None:
        messagebox.showwarning("Warning", "Please select an employee first")
        return

    answer = messagebox.askyesno(
        "Confirm", "Do you want to delete this employee?"
    )

    if answer:
        cur.execute(
            "DELETE FROM employee WHERE id=?",
            (selected_id,)
        )

        con.commit()
        read_data()
        clear_fields()

        messagebox.showinfo("Success", "Employee Deleted Successfully")


# Heading
Label(
    root,
    text="Employee Details Form",
    font=("Arial", 18, "bold"),
    bg="lightblue"
).pack(pady=10)


# Form Frame
form = Frame(root, bg="lightblue")
form.pack(pady=5)

Label(form, text="Employee Name:", bg="lightblue").grid(
    row=0, column=0, padx=5, pady=5, sticky="e"
)

name_entry = Entry(form, width=30)
name_entry.grid(row=0, column=1, padx=5, pady=5)

Label(form, text="Department:", bg="lightblue").grid(
    row=1, column=0, padx=5, pady=5, sticky="e"
)

dept_entry = Entry(form, width=30)
dept_entry.grid(row=1, column=1, padx=5, pady=5)

Label(form, text="Salary:", bg="lightblue").grid(
    row=2, column=0, padx=5, pady=5, sticky="e"
)

salary_entry = Entry(form, width=30)
salary_entry.grid(row=2, column=1, padx=5, pady=5)

Label(form, text="Phone:", bg="lightblue").grid(
    row=3, column=0, padx=5, pady=5, sticky="e"
)

phone_entry = Entry(form, width=30)
phone_entry.grid(row=3, column=1, padx=5, pady=5)


# Buttons
buttons = Frame(root, bg="lightblue")
buttons.pack(pady=10)

Button(buttons, text="CREATE", width=10,
       command=create_data).grid(row=0, column=0, padx=5)

Button(buttons, text="READ", width=10,
       command=read_data).grid(row=0, column=1, padx=5)

Button(buttons, text="UPDATE", width=10,
       command=update_data).grid(row=0, column=2, padx=5)

Button(buttons, text="DELETE", width=10,
       command=delete_data).grid(row=0, column=3, padx=5)

Button(buttons, text="CLEAR", width=10,
       command=clear_fields).grid(row=0, column=4, padx=5)


# Employee Records Table
tree = ttk.Treeview(
    root,
    columns=("ID", "Name", "Department", "Salary", "Phone"),
    show="headings",
    height=8
)

tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Department", text="Department")
tree.heading("Salary", text="Salary")
tree.heading("Phone", text="Phone")

tree.column("ID", width=40, anchor=CENTER)
tree.column("Name", width=150)
tree.column("Department", width=150)
tree.column("Salary", width=120)
tree.column("Phone", width=130)

tree.pack(padx=10, pady=10, fill=X)

tree.bind("<<TreeviewSelect>>", select_data)


# Display Existing Records
read_data()

root.mainloop()

con.close()
