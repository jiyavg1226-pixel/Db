
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database connection
conn = sqlite3.connect("hospital1.db")
cursor = conn.cursor()

# Create patient table
cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id TEXT,
    name TEXT,
    age INTEGER,
    gender TEXT,
    phone TEXT,
    disease TEXT
)
""")
conn.commit()

# Insert patient
def insert_data():
    if patient_id.get() == "" or name.get() == "":
        messagebox.showwarning("Warning", "Please enter Patient ID and Name")
        return

    cursor.execute("""
    INSERT INTO patients
    (patient_id, name, age, gender, phone, disease)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        patient_id.get(),
        name.get(),
        age.get(),
        gender.get(),
        phone.get(),
        disease.get()
    ))

    conn.commit()
    display_data()
    clear_data()
    messagebox.showinfo("Success", "Patient Registered Successfully")


# Display patients
def display_data():
    for row in tree.get_children():
        tree.delete(row)

    cursor.execute("SELECT * FROM patients")

    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)


# Select patient
def select_patient(event):
    selected = tree.focus()

    if selected:
        data = tree.item(selected, "values")

        clear_data()

        patient_id.insert(0, data[1])
        name.insert(0, data[2])
        age.insert(0, data[3])
        gender.set(data[4])
        phone.insert(0, data[5])
        disease.insert(0, data[6])


# Update patient
def update_data():
    selected = tree.focus()

    if not selected:
        messagebox.showwarning("Warning", "Please select a patient")
        return

    data = tree.item(selected, "values")

    cursor.execute("""
    UPDATE patients
    SET patient_id=?, name=?, age=?, gender=?, phone=?, disease=?
    WHERE id=?
    """, (
        patient_id.get(),
        name.get(),
        age.get(),
        gender.get(),
        phone.get(),
        disease.get(),
        data[0]
    ))

    conn.commit()
    display_data()
    clear_data()
    messagebox.showinfo("Success", "Patient Updated Successfully")


# Delete patient
def delete_data():
    selected = tree.focus()

    if not selected:
        messagebox.showwarning("Warning", "Please select a patient")
        return

    data = tree.item(selected, "values")

    cursor.execute("DELETE FROM patients WHERE id=?", (data[0],))

    conn.commit()
    display_data()
    clear_data()
    messagebox.showinfo("Success", "Patient Deleted Successfully")


# Clear fields
def clear_data():
    patient_id.delete(0, tk.END)
    name.delete(0, tk.END)
    age.delete(0, tk.END)
    gender.set("")
    phone.delete(0, tk.END)
    disease.delete(0, tk.END)


# Main window
root = tk.Tk()
root.title("Patient Registration System")
root.geometry("850x600")
root.configure(bg="ivory")

# Heading
tk.Label(
    root,
    text="PATIENT REGISTRATION SYSTEM",
    font=("Arial", 18, "bold"),
    bg="ivory",
    fg="darkblue"
).pack(pady=10)

# Form frame
frame = tk.Frame(root, bg="ivory")
frame.pack(pady=10)

# Patient ID
tk.Label(frame, text="Patient ID:", bg="ivory").grid(row=0, column=0, padx=10, pady=5)
patient_id = tk.Entry(frame)
patient_id.grid(row=0, column=1, padx=10, pady=5)

# Name
tk.Label(frame, text="Patient Name:", bg="ivory").grid(row=1, column=0, padx=10, pady=5)
name = tk.Entry(frame)
name.grid(row=1, column=1, padx=10, pady=5)

# Age
tk.Label(frame, text="Age:", bg="ivory").grid(row=2, column=0, padx=10, pady=5)
age = tk.Entry(frame)
age.grid(row=2, column=1, padx=10, pady=5)

# Gender
tk.Label(frame, text="Gender:", bg="ivory").grid(row=3, column=0, padx=10, pady=5)
gender = tk.StringVar()
ttk.Combobox(
    frame,
    textvariable=gender,
    values=["Male", "Female", "Other"],
    state="readonly"
).grid(row=3, column=1, padx=10, pady=5)

# Phone
tk.Label(frame, text="Phone:", bg="ivory").grid(row=4, column=0, padx=10, pady=5)
phone = tk.Entry(frame)
phone.grid(row=4, column=1, padx=10, pady=5)

# Disease
tk.Label(frame, text="Disease:", bg="ivory").grid(row=5, column=0, padx=10, pady=5)
disease = tk.Entry(frame)
disease.grid(row=5, column=1, padx=10, pady=5)

# Buttons
button_frame = tk.Frame(root, bg="ivory")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Insert", width=12, bg="lightgreen",
          command=insert_data).grid(row=0, column=0, padx=5)

tk.Button(button_frame, text="Update", width=12, bg="lightblue",
          command=update_data).grid(row=0, column=1, padx=5)

tk.Button(button_frame, text="Delete", width=12, bg="salmon",
          command=delete_data).grid(row=0, column=2, padx=5)

tk.Button(button_frame, text="Clear", width=12, bg="lightyellow",
          command=clear_data).grid(row=0, column=3, padx=5)

# Patient table
columns = ("ID", "Patient ID", "Name", "Age", "Gender", "Phone", "Disease")

tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=105)

tree.pack(fill="both", expand=True, padx=10, pady=10)

tree.bind("<<TreeviewSelect>>", select_patient)

# Display existing records
display_data()

root.mainloop()

conn.close()

