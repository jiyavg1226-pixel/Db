from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

# Database Connection
con = sqlite3.connect("member.db")
cur = con.cursor()

# Create Member Table
cur.execute("""
CREATE TABLE IF NOT EXISTS member (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    address TEXT NOT NULL
)
""")
con.commit()

selected_id = None

# Main Window
root = Tk()
root.title("Member Registration Form")
root.geometry("850x550")
root.configure(bg="pink")


# Clear All Fields
def clear_fields():
    global selected_id
    selected_id = None

    name_entry.delete(0, END)
    email_entry.delete(0, END)
    phone_entry.delete(0, END)
    address_entry.delete(0, END)


# Read Member Data
def read_data():
    for row in tree.get_children():
        tree.delete(row)

    cur.execute("SELECT * FROM member")
    rows = cur.fetchall()

    for row in rows:
        tree.insert("", END, values=row)


# Create Member
def create_data():
    name = name_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()
    address = address_entry.get()

    if name == "" or email == "" or phone == "" or address == "":
        messagebox.showwarning("Warning", "Please fill all fields")
        return

    cur.execute("""
        INSERT INTO member (name, email, phone, address)
        VALUES (?, ?, ?, ?)
    """, (name, email, phone, address))

    con.commit()

    messagebox.showinfo("Success", "Member Added Successfully")

    clear_fields()
    read_data()


# Select Member
def select_data(event):
    global selected_id

    selected = tree.focus()

    if selected == "":
        return

    values = tree.item(selected, "values")

    # Clear entries
    name_entry.delete(0, END)
    email_entry.delete(0, END)
    phone_entry.delete(0, END)
    address_entry.delete(0, END)

    selected_id = values[0]

    name_entry.insert(0, values[1])
    email_entry.insert(0, values[2])
    phone_entry.insert(0, values[3])
    address_entry.insert(0, values[4])


# Update Member
def update_data():
    if selected_id is None:
        messagebox.showwarning("Warning", "Please select a member")
        return

    name = name_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()
    address = address_entry.get()

    if name == "" or email == "" or phone == "" or address == "":
        messagebox.showwarning("Warning", "Please fill all fields")
        return

    cur.execute("""
        UPDATE member
        SET name=?, email=?, phone=?, address=?
        WHERE id=?
    """, (name, email, phone, address, selected_id))

    con.commit()

    messagebox.showinfo("Success", "Member Updated Successfully")

    clear_fields()
    read_data()


# Delete Member
def delete_data():
    if selected_id is None:
        messagebox.showwarning("Warning", "Please select a member")
        return

    answer = messagebox.askyesno(
        "Confirm",
        "Are you sure you want to delete?"
    )

    if answer:
        cur.execute("DELETE FROM member WHERE id=?", (selected_id,))
        con.commit()

        messagebox.showinfo("Success", "Member Deleted Successfully")

        clear_fields()
        read_data()


# Heading
title = Label(
    root,
    text="MEMBER REGISTRATION FORM",
    font=("Arial", 20, "bold"),
    bg="pink",
    fg="darkred"
)
title.pack(pady=15)


# Form Frame
form_frame = Frame(root, bg="pink")
form_frame.pack(pady=10)


# Member Name
Label(form_frame, text="Member Name:", font=("Arial", 12),
      bg="pink").grid(row=0, column=0, padx=10, pady=8)

name_entry = Entry(form_frame, font=("Arial", 12), width=25)
name_entry.grid(row=0, column=1, padx=10, pady=8)


# Email
Label(form_frame, text="Email:", font=("Arial", 12),
      bg="pink").grid(row=1, column=0, padx=10, pady=8)

email_entry = Entry(form_frame, font=("Arial", 12), width=25)
email_entry.grid(row=1, column=1, padx=10, pady=8)


# Phone
Label(form_frame, text="Phone:", font=("Arial", 12),
      bg="pink").grid(row=2, column=0, padx=10, pady=8)

phone_entry = Entry(form_frame, font=("Arial", 12), width=25)
phone_entry.grid(row=2, column=1, padx=10, pady=8)


# Address
Label(form_frame, text="Address:", font=("Arial", 12),
      bg="pink").grid(row=3, column=0, padx=10, pady=8)

address_entry = Entry(form_frame, font=("Arial", 12), width=25)
address_entry.grid(row=3, column=1, padx=10, pady=8)


# Buttons
button_frame = Frame(root, bg="pink")
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


# Member Table
tree = ttk.Treeview(
    root,
    columns=("ID", "Name", "Email", "Phone", "Address"),
    show="headings"
)

tree.heading("ID", text="ID")
tree.heading("Name", text="Member Name")
tree.heading("Email", text="Email")
tree.heading("Phone", text="Phone")
tree.heading("Address", text="Address")

tree.column("ID", width=50)
tree.column("Name", width=150)
tree.column("Email", width=180)
tree.column("Phone", width=120)
tree.column("Address", width=200)

tree.pack(pady=15, fill=X, padx=20)

# Select Row Event
tree.bind("<<TreeviewSelect>>", select_data)

# Display Existing Records
read_data()


# Close Database
def close_app():
    con.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", close_app)

# Run Application
root.mainloop()
