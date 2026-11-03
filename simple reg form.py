from tkinter import *
from tkinter import messagebox

# Create Main Window
root = Tk()
root.title("Student Registration Form")
root.geometry("400x450")
root.configure(bg="lightcyan")

# Heading
Label(root, text="REGISTRATION FORM",
      font=("Arial", 18, "bold"),
      bg="lightcyan").pack(pady=15)

# Name
Label(root, text="Name:", bg="lightcyan").pack()
name = Entry(root, width=30)
name.pack(pady=5)

# Email
Label(root, text="Email:", bg="lightcyan").pack()
email = Entry(root, width=30)
email.pack(pady=5)

# Gender
Label(root, text="Gender:", bg="lightcyan").pack()

gender = StringVar(value="Male")

Radiobutton(root, text="Male",
            variable=gender, value="Male",
            bg="lightcyan").pack()

Radiobutton(root, text="Female",
            variable=gender, value="Female",
            bg="lightcyan").pack()

# Course
Label(root, text="Course:", bg="lightcyan").pack()

course = StringVar(value="BCA")

OptionMenu(root, course, "BCA", "BBA", "BSC", "MCA").pack()

# Submit Function
def submit():
    messagebox.showinfo(
        "Registration Successful",
        "Name: " + name.get() +
        "\nEmail: " + email.get() +
        "\nGender: " + gender.get() +
        "\nCourse: " + course.get()
    )

# Submit Button
Button(root, text="Submit",
       command=submit,
       bg="green", fg="white",
       font=("Arial", 12, "bold")).pack(pady=15)

# Clear Function
def clear():
    name.delete(0, END)
    email.delete(0, END)
    phone.delete(0, END)
    gender.set("Male")
    course.set("BCA")

# Clear Button
Button(root, text="Clear",
       command=clear,
       bg="red", fg="white").pack()

# Run Application
root.mainloop()
