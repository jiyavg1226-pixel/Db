from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

# Database Connection
con = sqlite3.connect("patient.db")
cur = con.cursor()

# Create Patient Table
cur.execute("""
CREATE TABLE IF NOT EXISTS patient (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    gender TEXT NOT NULL,
    disease TEXT NOT NULL,
    phone TEXT NOT NULL,
    appointment TEXT NOT NULL
)
""")
con.commit()

selected_id = None

# Main Window
root = Tk()
root.title("Patient Registration Form")
root.geometry("950x650")
root.configure(bg="lavender")


# Clear All Fields
def clear_fields():
    global selected_id
    selected_id = None

    name_entry.delete(0, END)
    age_entry.delete(0, END)
    gender_combo.set("")
    disease_entry.delete(0, END)
    phone_entry.delete(0, END)
    appointment_entry.delete(0, END)


# Read Patient Data
def read_data():
    for row in tree.get_children():
        tree.delete(row)

    cur.execute("SELECT * FROM patient")
    rows = cur.fetchall()

    for row in rows:
        tree.insert("", END, values=row)


# Create Patient
def create_data():
    name = name_entry.get()
    age = age_entry.get()
    gender = gender_combo.get()
    disease = disease_entry.get()
    phone = phone_entry.get()
    appointment = appointment_entry.get()

    if name == "" or age == "" or gender == "" or disease == "" or phone == "" or appointment == "":
        messagebox.showwarning("Warning", "Please fill all fields")
        return

    if not age.isdigit() or int(age) <= 0:
        messagebox.showwarning("Warning", "Enter valid age")
        return

    cur.execute("""
        INSERT INTO patient
        (name, age, gender, disease, phone, appointment)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, int(age), gender, disease, phone, appointment))

    con.commit()

    messagebox.showinfo("Success", "Patient Added Successfully")

    clear_fields()
    read_data()


# Select Patient
def select_data(event):
    global selected_id

    selected = tree.focus()

    if selected == "":
        return

    values = tree.item(selected, "values")

    name_entry.delete(0, END)
    age_entry.delete(0, END)
    gender_combo.set("")
    disease_entry.delete(0, END)
    phone_entry.delete(0, END)
    appointment_entry.delete(0, END)

    selected_id = values[0]

    name_entry.insert(0, values[1])
    age_entry.insert(0, values[2])
    gender_combo.set(values[3])
    disease_entry.insert(0, values[4])
    phone_entry.insert(0, values[5])
    appointment_entry.insert(0, values[6])


# Update Patient
def update_data():
    if selected_id is None:
        messagebox.showwarning("Warning", "Please select a patient")
        return

    name = name_entry.get()
    age = age_entry.get()
    gender = gender_combo.get()
    disease = disease_entry.get()
    phone = phone_entry.get()
    appointment = appointment_entry.get()

    if name == "" or age == "" or gender == "" or disease == "" or phone == "" or appointment == "":
        messagebox.showwarning("Warning", "Please fill all fields")
        return

    if not age.isdigit() or int(age) <= 0:
        messagebox.showwarning("Warning", "Enter valid age")
        return

    cur.execute("""
        UPDATE patient
        SET name=?, age=?, gender=?, disease=?, phone=?, appointment=?
        WHERE id=?
    """, (name, int(age), gender, disease, phone, appointment, selected_id))

    con.commit()

    messagebox.showinfo("Success", "Patient Updated Successfully")

    clear_fields()
    read_data()


# Delete Patient
def delete_data():
    if selected_id is None:
        messagebox.showwarning("Warning", "Please select a patient")
        return

    answer = messagebox.askyesno(
        "Confirm",
        "Are you sure you want to delete?"
    )

    if answer:
        cur.execute("DELETE FROM patient WHERE id=?", (selected_id,))
        con.commit()

        messagebox.showinfo("Success", "Patient Deleted Successfully")

        clear_fields()
        read_data()


# Heading
title = Label(
    root,
    text="PATIENT REGISTRATION FORM",
    font=("Arial", 22, "bold"),
    bg="lavender",
    fg="purple"
)
title.pack(pady=15)


# Form Frame
form_frame = Frame(root, bg="lavender")
form_frame.pack(pady=10)


# Patient Name
Label(form_frame, text="Patient Name:", font=("Arial", 12),
      bg="lavender").grid(row=0, column=0, padx=10, pady=8)

name_entry = Entry(form_frame, font=("Arial", 12), width=25)
name_entry.grid(row=0, column=1, padx=10, pady=8)


# Age
Label(form_frame, text="Age:", font=("Arial", 12),
      bg="lavender").grid(row=1, column=0, padx=10, pady=8)

age_entry = Entry(form_frame, font=("Arial", 12), width=25)
age_entry.grid(row=1, column=1, padx=10, pady=8)


# Gender
Label(form_frame, text="Gender:", font=("Arial", 12),
      bg="lavender").grid(row=2, column=0, padx=10, pady=8)

gender_combo = ttk.Combobox(
    form_frame,
    font=("Arial", 12),
    width=23,
    values=("Male", "Female", "Other"),
    state="readonly"
)
gender_combo.grid(row=2, column=1, padx=10, pady=8)


# Disease
Label(form_frame, text="Disease:", font=("Arial", 12),
      bg="lavender").grid(row=3, column=0, padx=10, pady=8)

disease_entry = Entry(form_frame, font=("Arial", 12), width=25)
disease_entry.grid(row=3, column=1, padx=10, pady=8)


# Phone
Label(form_frame, text="Phone:", font=("Arial", 12),
      bg="lavender").grid(row=4, column=0, padx=10, pady=8)

phone_entry = Entry(form_frame, font=("Arial", 12), width=25)
phone_entry.grid(row=4, column=1, padx=10, pady=8)


# Appointment
Label(form_frame, text="Appointment:", font=("Arial", 12),
      bg="lavender").grid(row=5, column=0, padx=10, pady=8)

appointment_entry = Entry(form_frame, font=("Arial", 12), width=25)
appointment_entry.grid(row=5, column=1, padx=10, pady=8)


# Buttons
button_frame = Frame(root, bg="lavender")
button_frame.pack(pady=10)

Button(button_frame, text="CREATE", width=12,
       bg="plum", command=create_data).grid(row=0, column=0, padx=5)

Button(button_frame, text="READ", width=12,
       bg="plum", command=read_data).grid(row=0, column=1, padx=5)

Button(button_frame, text="UPDATE", width=12,
       bg="plum", command=update_data).grid(row=0, column=2, padx=5)

Button(button_frame, text="DELETE", width=12,
       bg="plum", command=delete_data).grid(row=0, column=3, padx=5)

Button(button_frame, text="CLEAR", width=12,
       bg="plum", command=clear_fields).grid(row=0, column=4, padx=5)


# Patient Table
tree = ttk.Treeview(
    root,
    columns=("ID", "Name", "Age", "Gender", "Disease", "Phone", "Appointment"),
    show="headings"
)

tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Age", text="Age")
tree.heading("Gender", text="Gender")
tree.heading("Disease", text="Disease")
tree.heading("Phone", text="Phone")
tree.heading("Appointment", text="Appointment")

tree.column("ID", width=40)
tree.column("Name", width=120)
tree.column("Age", width=50)
tree.column("Gender", width=80)
tree.column("Disease", width=120)
tree.column("Phone", width=110)
tree.column("Appointment", width=140)

tree.pack(pady=15, fill=X, padx=15)

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
