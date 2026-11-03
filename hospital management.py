from tkinter import *
from tkinter import ttk, messagebox
from pymongo import MongoClient

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")

db = client["HospitalDB"]
collection = db["patients"]

# Main Window
root = Tk()
root.title("Hospital Management System")
root.geometry("1050x780")
root.configure(bg="lavender")


# Clear Fields
def clear_fields():

    id_entry.delete(0, END)
    name_entry.delete(0, END)
    age_entry.delete(0, END)
    disease_entry.delete(0, END)
    room_combo.set("")
    days_entry.delete(0, END)
    charge_entry.delete(0, END)
    total_entry.delete(0, END)


# Display Patient Data
def read_data():

    for row in tree.get_children():
        tree.delete(row)

    patients = collection.find()

    for patient in patients:
        tree.insert("", END, values=(
            patient["patient_id"],
            patient["name"],
            patient["age"],
            patient["disease"],
            patient["room"],
            patient["days"],
            patient["room_charge"]
        ))


# Add Patient
def add_patient():

    patient_id = id_entry.get()
    name = name_entry.get()
    age = age_entry.get()
    disease = disease_entry.get()
    room = room_combo.get()
    days = days_entry.get()
    charge = charge_entry.get()

    if (patient_id == "" or name == "" or age == "" or
        disease == "" or room == "" or days == "" or charge == ""):

        messagebox.showwarning("Warning", "Please fill all fields")
        return

    if not age.isdigit() or int(age) <= 0:
        messagebox.showwarning("Warning", "Enter valid age")
        return

    try:
        days_value = int(days)
        charge_value = float(charge)

        if days_value <= 0 or charge_value < 0:
            raise ValueError

    except ValueError:
        messagebox.showwarning("Warning", "Enter valid days and charge")
        return

    # Check Duplicate Patient ID
    if collection.find_one({"patient_id": patient_id}):
        messagebox.showerror("Error", "Patient ID already exists")
        return

    patient = {
        "patient_id": patient_id,
        "name": name,
        "age": int(age),
        "disease": disease,
        "room": room,
        "days": days_value,
        "room_charge": charge_value
    }

    collection.insert_one(patient)

    messagebox.showinfo("Success", "Patient Added Successfully")

    read_data()
    clear_fields()


# Search Patient
def search_patient():

    patient_id = id_entry.get().strip()
    name = name_entry.get().strip()

    if patient_id != "":
        patient = collection.find_one({"patient_id": patient_id})

    elif name != "":
        patient = collection.find_one({
            "name": {"$regex": "^" + name + "$", "$options": "i"}
        })

    else:
        messagebox.showwarning("Warning", "Enter Patient ID or Name")
        return

    if patient:

        clear_fields()

        id_entry.insert(0, patient["patient_id"])
        name_entry.insert(0, patient["name"])
        age_entry.insert(0, patient["age"])
        disease_entry.insert(0, patient["disease"])
        room_combo.set(patient["room"])
        days_entry.insert(0, patient["days"])
        charge_entry.insert(0, patient["room_charge"])

        messagebox.showinfo("Success", "Patient Found")

    else:
        messagebox.showerror("Error", "Patient Not Found")


# Select Patient From Table
def select_patient(event):

    selected = tree.focus()

    if selected == "":
        return

    values = tree.item(selected, "values")

    clear_fields()

    id_entry.insert(0, values[0])
    name_entry.insert(0, values[1])
    age_entry.insert(0, values[2])
    disease_entry.insert(0, values[3])
    room_combo.set(values[4])
    days_entry.insert(0, values[5])
    charge_entry.insert(0, values[6])


# Calculate Bill
def calculate_bill():

    try:
        days = int(days_entry.get())
        charge = float(charge_entry.get())

        if days <= 0 or charge < 0:
            raise ValueError

        total = days * charge

        total_entry.delete(0, END)
        total_entry.insert(0, str(total))

        messagebox.showinfo(
            "Hospital Bill",
            f"Room Charges: {days} x {charge}\n"
            f"Total Bill: Rs. {total:.2f}"
        )

    except ValueError:
        messagebox.showwarning(
            "Warning",
            "Enter valid number of days and room charge"
        )


# Heading
Label(
    root,
    text="HOSPITAL MANAGEMENT SYSTEM",
    font=("Arial", 22, "bold"),
    bg="lavender",
    fg="purple"
).pack(pady=15)


# Form Frame
form = Frame(root, bg="lavender")
form.pack(pady=5)


# Patient ID
Label(form, text="Patient ID:", bg="lavender",
      font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=6)

id_entry = Entry(form, width=25, font=("Arial", 12))
id_entry.grid(row=0, column=1, padx=10, pady=6)


# Patient Name
Label(form, text="Patient Name:", bg="lavender",
      font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=6)

name_entry = Entry(form, width=25, font=("Arial", 12))
name_entry.grid(row=1, column=1, padx=10, pady=6)


# Age
Label(form, text="Age:", bg="lavender",
      font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=6)

age_entry = Entry(form, width=25, font=("Arial", 12))
age_entry.grid(row=2, column=1, padx=10, pady=6)


# Disease
Label(form, text="Disease:", bg="lavender",
      font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=6)

disease_entry = Entry(form, width=25, font=("Arial", 12))
disease_entry.grid(row=3, column=1, padx=10, pady=6)


# Room Type
Label(form, text="Room Type:", bg="lavender",
      font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=6)

room_combo = ttk.Combobox(
    form,
    values=["General", "Semi-Private", "Private"],
    width=23,
    state="readonly"
)
room_combo.grid(row=4, column=1, padx=10, pady=6)


# Number of Days
Label(form, text="Number of Days:", bg="lavender",
      font=("Arial", 12)).grid(row=5, column=0, padx=10, pady=6)

days_entry = Entry(form, width=25, font=("Arial", 12))
days_entry.grid(row=5, column=1, padx=10, pady=6)


# Room Charge
Label(form, text="Room Charge Per Day:", bg="lavender",
      font=("Arial", 12)).grid(row=6, column=0, padx=10, pady=6)

charge_entry = Entry(form, width=25, font=("Arial", 12))
charge_entry.grid(row=6, column=1, padx=10, pady=6)


# Total Bill
Label(form, text="Total Bill:", bg="lavender",
      font=("Arial", 12)).grid(row=7, column=0, padx=10, pady=6)

total_entry = Entry(form, width=25, font=("Arial", 12))
total_entry.grid(row=7, column=1, padx=10, pady=6)


# Buttons
button_frame = Frame(root, bg="lavender")
button_frame.pack(pady=12)

Button(button_frame, text="ADD PATIENT",
       width=15, bg="plum",
       command=add_patient).grid(row=0, column=0, padx=5)

Button(button_frame, text="SEARCH",
       width=15, bg="plum",
       command=search_patient).grid(row=0, column=1, padx=5)

Button(button_frame, text="CALCULATE BILL",
       width=15, bg="plum",
       command=calculate_bill).grid(row=0, column=2, padx=5)

Button(button_frame, text="CLEAR",
       width=15, bg="plum",
       command=clear_fields).grid(row=0, column=3, padx=5)


# Patient Details Heading
Label(
    root,
    text="PATIENT DETAILS",
    font=("Arial", 16, "bold"),
    bg="lavender",
    fg="purple"
).pack(pady=8)


# Table Frame
table_frame = Frame(root, bg="lavender")
table_frame.pack(fill=BOTH, expand=True, padx=15, pady=10)


# Patient Details Table
tree = ttk.Treeview(
    table_frame,
    columns=("ID", "Name", "Age", "Disease",
             "Room", "Days", "Charge"),
    show="headings",
    height=8
)

tree.heading("ID", text="Patient ID")
tree.heading("Name", text="Name")
tree.heading("Age", text="Age")
tree.heading("Disease", text="Disease")
tree.heading("Room", text="Room")
tree.heading("Days", text="Days")
tree.heading("Charge", text="Room Charge")

tree.column("ID", width=90)
tree.column("Name", width=130)
tree.column("Age", width=60)
tree.column("Disease", width=130)
tree.column("Room", width=110)
tree.column("Days", width=60)
tree.column("Charge", width=120)

tree.pack(fill=BOTH, expand=True)

# Select Table Row
tree.bind("<<TreeviewSelect>>", select_patient)


# Display Existing Records
read_data()


# Close Database
def close_app():
    client.close()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", close_app)

# Run Application
root.mainloop()
