
import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database connection
conn = sqlite3.connect("member1.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    username TEXT UNIQUE,
    password TEXT
)
""")
conn.commit()


# Registration function
def register():
    name = name_entry.get()
    email = email_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    if name == "" or email == "" or username == "" or password == "":
        messagebox.showwarning("Warning", "Please fill all fields")
        return

    try:
        cursor.execute("""
        INSERT INTO members (name, email, username, password)
        VALUES (?, ?, ?, ?)
        """, (name, email, username, password))

        conn.commit()
        messagebox.showinfo("Success", "Member Registered Successfully")
        clear_fields()

    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists")


# Clear registration fields
def clear_fields():
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)


# Login function
def login():
    username = login_username.get()
    password = login_password.get()

    cursor.execute("""
    SELECT * FROM members
    WHERE username=? AND password=?
    """, (username, password))

    member = cursor.fetchone()

    if member:
        messagebox.showinfo("Login Successful", "Welcome " + member[1])
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password")


# Main window
root = tk.Tk()
root.title("Member Registration and Login System")
root.geometry("500x600")
root.configure(bg="ivory")

# Heading
tk.Label(
    root,
    text="MEMBER REGISTRATION SYSTEM",
    font=("Arial", 18, "bold"),
    bg="ivory",
    fg="darkblue"
).pack(pady=15)

# Registration frame
reg_frame = tk.LabelFrame(
    root,
    text="Member Registration",
    font=("Arial", 12, "bold"),
    bg="ivory",
    padx=15,
    pady=15
)
reg_frame.pack(padx=20, pady=10, fill="x")

tk.Label(reg_frame, text="Name:", bg="ivory").grid(row=0, column=0, pady=8)
name_entry = tk.Entry(reg_frame, width=30)
name_entry.grid(row=0, column=1)

tk.Label(reg_frame, text="Email:", bg="ivory").grid(row=1, column=0, pady=8)
email_entry = tk.Entry(reg_frame, width=30)
email_entry.grid(row=1, column=1)

tk.Label(reg_frame, text="Username:", bg="ivory").grid(row=2, column=0, pady=8)
username_entry = tk.Entry(reg_frame, width=30)
username_entry.grid(row=2, column=1)

tk.Label(reg_frame, text="Password:", bg="ivory").grid(row=3, column=0, pady=8)
password_entry = tk.Entry(reg_frame, width=30, show="*")
password_entry.grid(row=3, column=1)

tk.Button(
    reg_frame,
    text="Register",
    bg="lightgreen",
    width=15,
    command=register
).grid(row=4, column=1, pady=12)


# Login frame
login_frame = tk.LabelFrame(
    root,
    text="Member Login",
    font=("Arial", 12, "bold"),
    bg="ivory",
    padx=15,
    pady=15
)
login_frame.pack(padx=20, pady=10, fill="x")

tk.Label(login_frame, text="Username:", bg="ivory").grid(row=0, column=0, pady=8)
login_username = tk.Entry(login_frame, width=30)
login_username.grid(row=0, column=1)

tk.Label(login_frame, text="Password:", bg="ivory").grid(row=1, column=0, pady=8)
login_password = tk.Entry(login_frame, width=30, show="*")
login_password.grid(row=1, column=1)

tk.Button(
    login_frame,
    text="Login",
    bg="lightblue",
    width=15,
    command=login
).grid(row=2, column=1, pady=12)


root.mainloop()
conn.close()
