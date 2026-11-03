
from tkinter import *
from tkinter import messagebox

# Main Window
root = Tk()
root.title("Student Information Form")
root.geometry("500x750")
root.configure(bg="lightyellow")

# Heading
Label(root, text="STUDENT REGISTRATION FORM",
      font=("Arial", 16, "bold"),
      bg="lightyellow").pack(pady=10)

# Name
Label(root, text="Name:", bg="lightyellow").pack()
name_entry = Entry(root, width=30)
name_entry.pack(pady=5)

# Email
Label(root, text="Email:", bg="lightyellow").pack()
email_entry = Entry(root, width=30)
email_entry.pack(pady=5)

# Phone
Label(root, text="Phone:", bg="lightyellow").pack()
phone_entry = Entry(root, width=30)
phone_entry.pack(pady=5)

# Address
Label(root, text="Address:", bg="lightyellow").pack()
address_entry = Entry(root, width=30)
address_entry.pack(pady=5)

# Class Name (Radio Buttons)
Label(root, text="Class Name:", bg="lightyellow").pack()

class_var = StringVar(value="BCA")

Radiobutton(root, text="BCA", variable=class_var,
            value="BCA", bg="lightyellow").pack()

Radiobutton(root, text="BBA", variable=class_var,
            value="BBA", bg="lightyellow").pack()

Radiobutton(root, text="BSC", variable=class_var,
            value="BSC", bg="lightyellow").pack()

# Semester (Listbox)
Label(root, text="Semester:", bg="lightyellow").pack()

semester_list = Listbox(root, height=4, width=20)

for sem in ["Semester 1", "Semester 2",
            "Semester 3", "Semester 4",
            "Semester 5", "Semester 6"]:
    semester_list.insert(END, sem)

semester_list.pack(pady=5)

# Hobbies (Checkboxes)
Label(root, text="Hobbies:", bg="lightyellow").pack()

hobby1 = IntVar()
hobby2 = IntVar()
hobby3 = IntVar()

Checkbutton(root, text="Reading", variable=hobby1,
            bg="lightyellow").pack()

Checkbutton(root, text="Playing", variable=hobby2,
            bg="lightyellow").pack()

Checkbutton(root, text="Music", variable=hobby3,
            bg="lightyellow").pack()

# Image (Canvas)
Label(root, text="Student Image:", bg="lightyellow").pack()

canvas = Canvas(root, width=100, height=60, bg="white")
canvas.pack(pady=5)

canvas.create_text(50, 30, text="Image")

# Submit Function
def submit():

    name = name_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()
    address = address_entry.get()

    selected_sem = semester_list.curselection()

    if selected_sem:
        semester = semester_list.get(selected_sem[0])
    else:
        semester = "Not Selected"

    hobbies = []

    if hobby1.get():
        hobbies.append("Reading")

    if hobby2.get():
        hobbies.append("Playing")

    if hobby3.get():
        hobbies.append("Music")

    messagebox.showinfo(
        "Student Information",
        f"Name: {name}\n"
        f"Email: {email}\n"
        f"Phone: {phone}\n"
        f"Address: {address}\n"
        f"Class: {class_var.get()}\n"
        f"Semester: {semester}\n"
        f"Hobbies: {', '.join(hobbies)}"
    )

# Submit Button
Button(root, text="Submit",
       command=submit,
       bg="green",
       fg="white",
       font=("Arial", 12, "bold")).pack(pady=15)

# Run Application
root.mainloop()

