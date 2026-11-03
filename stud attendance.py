from tkinter import *
from tkinter import ttk, messagebox
from pymongo import MongoClient

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")

db = client["AttendanceDB"]
collection = db["students"]

# Main Window
root = Tk()
root.title("Student Attendance Management System")
root.geometry("950x700")
root.configure(bg="lavender")


# Clear Fields
def clear_fields():

    id_entry.delete(0, END)
    name_entry.delete(0, END)
    course_entry.delete(0, END)
    total_entry.delete(0, END)
    present_entry.delete(0, END)
    percentage_entry.delete(0, END)


# Calculate Attendance Percentage
def calculate_percentage():

    try:
        total = int(total_entry.get())
        present = int(present_entry.get())

        if total <= 0 or present < 0 or present > total:
            messagebox.showwarning(
                "Warning",
                "Enter valid attendance days"
            )
            return

        percentage = (present / total) * 100

        percentage_entry.delete(0, END)
        percentage_entry.insert(0, f"{percentage:.2f}%")

    except ValueError:
        messagebox.showwarning(
            "Warning",
            "Enter valid numbers"
        )


# Insert Student Attendance
def insert_data():

    student_id = id_entry.get()
    name = name_entry.get()
    course = course_entry.get()
    total = total_entry.get()
    present = present_entry.get()

    if student_id == "" or name == "" or course == "" or total == "" or present == "":
        messagebox.showwarning("Warning", "Please fill all fields")
        return

    try:
        total = int(total)
        present = int(present)

        if total <= 0 or present < 0 or present > total:
            messagebox.showwarning(
                "Warning",
                "Enter valid attendance days"
            )
            return

    except ValueError:
        messagebox.showwarning("Warning", "Enter valid numbers")
        return

    # Check Duplicate Student ID
    if collection.find_one({"student_id": student_id}):
        messagebox.showerror("Error", "Student ID Already Exists")
        return

    percentage = (present / total) * 100

    data = {
        "student_id": student_id,
        "name": name,
        "course": course,
        "total_days": total,
        "present_days": present,
        "percentage": percentage
    }

    collection.insert_one(data)

    messagebox.showinfo(
        "Success",
        "Attendance Added Successfully"
    )

    clear_fields()
    display_data()


# Search Student
def search_data():

    student_id = id_entry.get()
    name = name_entry.get()

    if student_id != "":
        data = collection.find_one({"student_id": student_id})

    elif name != "":
        data = collection.find_one({
            "name": {"$regex": "^" + name + "$", "$options": "i"}
        })

    else:
        messagebox.showwarning(
            "Warning",
            "Enter Student ID or Name"
        )
        return

    if data:

        clear_fields()

        id_entry.insert(0, data["student_id"])
        name_entry.insert(0, data["name"])
        course_entry.insert(0, data["course"])
        total_entry.insert(0, data["total_days"])
        present_entry.insert(0, data["present_days"])
        percentage_entry.insert(
            0,
            f"{data['percentage']:.2f}%"
        )

        messagebox.showinfo("Success", "Student Found")

    else:
        messagebox.showerror("Error", "Student Not Found")


# Update Attendance
def update_data():

    student_id = id_entry.get()

    if student_id == "":
        messagebox.showwarning("Warning", "Enter Student ID")
        return

    data = collection.find_one({"student_id": student_id})

    if data is None:
        messagebox.showerror("Error", "Student Not Found")
        return

    name = name_entry.get()
    course = course_entry.get()
    total = total_entry.get()
    present = present_entry.get()

    if name == "" or course == "" or total == "" or present == "":
        messagebox.showwarning("Warning", "Please fill all fields")
        return

    try:
        total = int(total)
        present = int(present)

        if total <= 0 or present < 0 or present > total:
            messagebox.showwarning(
                "Warning",
                "Enter valid attendance days"
            )
            return

    except ValueError:
        messagebox.showwarning("Warning", "Enter valid numbers")
        return

    percentage = (present / total) * 100

    collection.update_one(
        {"student_id": student_id},
        {"$set": {
            "name": name,
            "course": course,
            "total_days": total,
            "present_days": present,
            "percentage": percentage
        }}
    )

    messagebox.showinfo(
        "Success",
        "Attendance Updated Successfully"
    )

    clear_fields()
    display_data()


# Delete Student
def delete_data():

    student_id = id_entry.get()

    if student_id == "":
        messagebox.showwarning("Warning", "Enter Student ID")
        return

    data = collection.find_one({"student_id": student_id})

    if data is None:
        messagebox.showerror("Error", "Student Not Found")
        return

    answer = messagebox.askyesno(
        "Confirm",
        "Are you sure you want to delete?"
    )

    if answer:
        collection.delete_one({"student_id": student_id})

        messagebox.showinfo(
            "Success",
            "Student Deleted Successfully"
        )

        clear_fields()
        display_data()


# Display All Students
def display_data():

    for row in tree.get_children():
        tree.delete(row)

    records = collection.find()

    for data in records:

        tree.insert("", END, values=(
            data["student_id"],
            data["name"],
            data["course"],
            data["total_days"],
            data["present_days"],
            f"{data['percentage']:.2f}%"
        ))


# Select Student
def select_data(event):

    selected = tree.focus()

    if selected == "":
        return

    values = tree.item(selected, "values")

    clear_fields()

    id_entry.insert(0, values[0])
    name_entry.insert(0, values[1])
    course_entry.insert(0, values[2])
    total_entry.insert(0, values[3])
    present_entry.insert(0, values[4])
    percentage_entry.insert(0, values[5])


# Heading
Label(
    root,
    text="STUDENT ATTENDANCE MANAGEMENT SYSTEM",
    font=("Arial", 21, "bold"),
    bg="lavender",
    fg="purple"
).pack(pady=15)


# Form Frame
form = Frame(root, bg="lavender")
form.pack(pady=10)


# Student ID
Label(form, text="Student ID:", bg="lavender",
      font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=8)

id_entry = Entry(form, width=25, font=("Arial", 12))
id_entry.grid(row=0, column=1)


# Student Name
Label(form, text="Student Name:", bg="lavender",
      font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=8)

name_entry = Entry(form, width=25, font=("Arial", 12))
name_entry.grid(row=1, column=1)


# Course
Label(form, text="Course:", bg="lavender",
      font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=8)

course_entry = Entry(form, width=25, font=("Arial", 12))
course_entry.grid(row=2, column=1)


# Total Days
Label(form, text="Total Working Days:", bg="lavender",
      font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=8)

total_entry = Entry(form, width=25, font=("Arial", 12))
total_entry.grid(row=3, column=1)


# Present Days
Label(form, text="Present Days:", bg="lavender",
      font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=8)

present_entry = Entry(form, width=25, font=("Arial", 12))
present_entry.grid(row=4, column=1)


# Attendance Percentage
Label(form, text="Attendance Percentage:", bg="lavender",
      font=("Arial", 12)).grid(row=5, column=0, padx=10, pady=8)

percentage_entry = Entry(form, width=25, font=("Arial", 12))
percentage_entry.grid(row=5, column=1)


# Buttons
button_frame = Frame(root, bg="lavender")
button_frame.pack(pady=15)

Button(button_frame, text="INSERT", width=13,
       bg="plum", command=insert_data).grid(row=0, column=0, padx=5, pady=5)

Button(button_frame, text="UPDATE", width=13,
       bg="plum", command=update_data).grid(row=0, column=1, padx=5, pady=5)

Button(button_frame, text="DELETE", width=13,
       bg="plum", command=delete_data).grid(row=0, column=2, padx=5, pady=5)

Button(button_frame, text="SEARCH", width=13,
       bg="plum", command=search_data).grid(row=0, column=3, padx=5, pady=5)

Button(button_frame, text="DISPLAY", width=13,
       bg="plum", command=display_data).grid(row=0, column=4, padx=5, pady=5)

Button(button_frame, text="CALCULATE", width=13,
       bg="plum", command=calculate_percentage).grid(row=1, column=1, padx=5, pady=5)

Button(button_frame, text="CLEAR", width=13,
       bg="plum", command=clear_fields).grid(row=1, column=2, padx=5, pady=5)


# Student Attendance Table
tree = ttk.Treeview(
    root,
    columns=("ID", "Name", "Course", "Total", "Present", "Percentage"),
    show="headings"
)

tree.heading("ID", text="Student ID")
tree.heading("Name", text="Student Name")
tree.heading("Course", text="Course")
tree.heading("Total", text="Total Days")
tree.heading("Present", text="Present Days")
tree.heading("Percentage", text="Attendance %")

tree.column("ID", width=100)
tree.column("Name", width=150)
tree.column("Course", width=120)
tree.column("Total", width=100)
tree.column("Present", width=100)
tree.column("Percentage", width=130)

tree.pack(pady=15, fill=X, padx=15)

# Select Row Event
tree.bind("<<TreeviewSelect>>", select_data)

# Display Existing Records
display_data()


# Close Application
def close_app():
    client.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", close_app)

# Run Application
root.mainloop()
