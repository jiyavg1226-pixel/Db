from tkinter import *
from tkinter import ttk, messagebox
from pymongo import MongoClient


# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["StudentDB"]
collection = db["stud"]

# Main Window
root = Tk()
root.title("Student Record Management System")
root.geometry("1150x750")
root.configure(bg="lavender")

# Heading
Label(
    root,
    text="Student Record Management System",
    font=("Arial", 20, "bold"),
    bg="lavender",
    fg="purple"
).pack(pady=10)

# Variables
sid = StringVar()
name = StringVar()
course = StringVar()

mean_stack = StringVar()
networking = StringVar()
cloud = StringVar()
machine_learning = StringVar()

total = StringVar()
percentage = StringVar()
grade = StringVar()

# Form Frame
frame = Frame(root, bg="lavender")
frame.pack(pady=10)


# Create Entry Fields
def create_field(label, variable, row, col):
    Label(
        frame,
        text=label,
        font=("Arial", 11, "bold"),
        bg="lavender"
    ).grid(row=row, column=col, padx=10, pady=7)

    Entry(
        frame,
        textvariable=variable,
        font=("Arial", 11),
        width=20
    ).grid(row=row, column=col+1, padx=10, pady=7)


# Student Details
create_field("Student ID", sid, 0, 0)
create_field("Student Name", name, 0, 2)

create_field("Course", course, 1, 0)

# Subject Marks
create_field("Mean Stack Marks", mean_stack, 2, 0)
create_field("Computer Networking", networking, 2, 2)

create_field("Cloud Computing", cloud, 3, 0)
create_field("Machine Learning", machine_learning, 3, 2)

# Result Details
create_field("Total Marks", total, 4, 0)
create_field("Percentage", percentage, 4, 2)

create_field("Grade", grade, 5, 0)


# Calculate Function
def calculate():
    try:
        m = float(mean_stack.get())
        n = float(networking.get())
        c = float(cloud.get())
        ml = float(machine_learning.get())

        marks = [m, n, c, ml]

        if any(x < 0 or x > 100 for x in marks):
            messagebox.showerror(
                "Error",
                "Marks must be between 0 and 100."
            )
            return None

        t = sum(marks)
        p = (t / 400) * 100

        if p >= 90:
            gr = "A+"
        elif p >= 80:
            gr = "A"
        elif p >= 70:
            gr = "B"
        elif p >= 60:
            gr = "C"
        elif p >= 50:
            gr = "D"
        else:
            gr = "F"

        total.set(f"{t:.2f}")
        percentage.set(f"{p:.2f}%")
        grade.set(gr)

        return {
            "total": t,
            "percentage": p,
            "grade": gr
        }

    except ValueError:
        messagebox.showerror(
            "Error",
            "Please enter valid marks."
        )
        return None


# Clear Function
def clear():
    sid.set("")
    name.set("")
    course.set("")

    mean_stack.set("")
    networking.set("")
    cloud.set("")
    machine_learning.set("")

    total.set("")
    percentage.set("")
    grade.set("")


# Add Function
def add():
    try:
        student_id = sid.get().strip()

        if not student_id or not name.get().strip() or not course.get().strip():
            messagebox.showerror(
                "Error",
                "Please fill Student ID, Name and Course."
            )
            return

        if collection.find_one({"sid": student_id}):
            messagebox.showerror(
                "Error",
                "Student ID already exists."
            )
            return

        result = calculate()

        if result is None:
            return

        data = {
            "sid": student_id,
            "name": name.get().strip(),
            "course": course.get().strip(),

            "mean_stack": float(mean_stack.get()),
            "networking": float(networking.get()),
            "cloud": float(cloud.get()),
            "machine_learning": float(machine_learning.get()),

            "total": result["total"],
            "percentage": result["percentage"],
            "grade": result["grade"]
        }

        collection.insert_one(data)

        messagebox.showinfo(
            "Success",
            "Student record added successfully!"
        )

        display()
        clear()

    except Exception as e:
        messagebox.showerror("Error", str(e))


# Update Function
def update():
    try:
        student_id = sid.get().strip()

        if not student_id:
            messagebox.showerror(
                "Error",
                "Enter Student ID."
            )
            return

        if not name.get().strip() or not course.get().strip():
            messagebox.showerror(
                "Error",
                "Please fill Student Name and Course."
            )
            return

        result = calculate()

        if result is None:
            return

        data = {
            "name": name.get().strip(),
            "course": course.get().strip(),

            "mean_stack": float(mean_stack.get()),
            "networking": float(networking.get()),
            "cloud": float(cloud.get()),
            "machine_learning": float(machine_learning.get()),

            "total": result["total"],
            "percentage": result["percentage"],
            "grade": result["grade"]
        }

        res = collection.update_one(
            {"sid": student_id},
            {"$set": data}
        )

        if res.matched_count > 0:
            messagebox.showinfo(
                "Success",
                "Student record updated successfully!"
            )
            display()
            clear()

        else:
            messagebox.showerror(
                "Error",
                "Student ID not found."
            )

    except Exception as e:
        messagebox.showerror("Error", str(e))


# Delete Function
def delete():
    student_id = sid.get().strip()

    if not student_id:
        messagebox.showerror(
            "Error",
            "Enter Student ID."
        )
        return

    confirm = messagebox.askyesno(
        "Confirm",
        "Do you want to delete this student?"
    )

    if confirm:
        res = collection.delete_one(
            {"sid": student_id}
        )

        if res.deleted_count > 0:
            messagebox.showinfo(
                "Success",
                "Student deleted successfully!"
            )
            display()
            clear()

        else:
            messagebox.showerror(
                "Error",
                "Student ID not found."
            )


# Search Function
def search():
    student_id = sid.get().strip()
    student_name = name.get().strip()

    if student_id:
        data = collection.find_one(
            {"sid": student_id}
        )

    elif student_name:
        data = collection.find_one({
            "name": {
                "$regex": "^" + student_name + "$",
                "$options": "i"
            }
        })

    else:
        messagebox.showerror(
            "Error",
            "Enter Student ID or Name."
        )
        return

    if data:
        clear()

        sid.set(data["sid"])
        name.set(data["name"])
        course.set(data["course"])

        mean_stack.set(str(data["mean_stack"]))
        networking.set(str(data["networking"]))
        cloud.set(str(data["cloud"]))
        machine_learning.set(str(data["machine_learning"]))

        total.set(str(data["total"]))
        percentage.set(f'{data["percentage"]:.2f}%')
        grade.set(data["grade"])

    else:
        messagebox.showerror(
            "Error",
            "Student not found."
        )


# Display Function
def display():
    for row in tree.get_children():
        tree.delete(row)

    for data in collection.find():
        tree.insert("", END, values=(
            data["sid"],
            data["name"],
            data["course"],
            data["total"],
            f'{data["percentage"]:.2f}%',
            data["grade"]
        ))


# Select Record
def select_record(event):
    selected = tree.focus()

    if selected:
        values = tree.item(selected, "values")

        student = collection.find_one(
            {"sid": values[0]}
        )

        if student:
            clear()

            sid.set(student["sid"])
            name.set(student["name"])
            course.set(student["course"])

            mean_stack.set(str(student["mean_stack"]))
            networking.set(str(student["networking"]))
            cloud.set(str(student["cloud"]))
            machine_learning.set(str(student["machine_learning"]))

            total.set(str(student["total"]))
            percentage.set(f'{student["percentage"]:.2f}%')
            grade.set(student["grade"])


# Exit Function
def exit_app():
    client.close()
    root.destroy()


# Buttons Frame
button_frame = Frame(root, bg="lavender")
button_frame.pack(pady=10)

buttons = [
    ("CALCULATE", calculate),
    ("INSERT", add),
    ("UPDATE", update),
    ("DELETE", delete),
    ("SEARCH", search),
    ("CLEAR", clear),
    ("EXIT", exit_app)
]

for i, (text, command) in enumerate(buttons):
    Button(
        button_frame,
        text=text,
        command=command,
        bg="plum",
        fg="black",
        font=("Arial", 10, "bold"),
        width=12
    ).grid(row=0, column=i, padx=4, pady=5)


# Table Frame
table_frame = Frame(root)
table_frame.pack(pady=15, fill=BOTH, expand=True)

columns = (
    "Student ID",
    "Name",
    "Course",
    "Total Marks",
    "Percentage",
    "Grade"
)

tree = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150, anchor=CENTER)

tree.pack(fill=BOTH, expand=True)

tree.bind("<<TreeviewSelect>>", select_record)


# Close Window
root.protocol("WM_DELETE_WINDOW", exit_app)

# Run Application
root.mainloop()
