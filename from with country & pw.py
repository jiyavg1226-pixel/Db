from tkinter import *
from tkinter import messagebox

# Main Window
root = Tk()
root.title("Registration Form")
root.geometry("450x550")
root.configure(bg="lightblue")

# Heading
Label(root, text="REGISTRATION FORM",
      font=("Arial", 20, "bold"),
      bg="darkblue", fg="white",
      width=30).pack(pady=15)

# Name
Label(root, text="Name:",
      bg="lightblue", fg="black").pack()

name = Entry(root, width=30)
name.pack(pady=5)

# Email
Label(root, text="Email:",
      bg="lightblue").pack()

email = Entry(root, width=30)
email.pack(pady=5)

# Password
Label(root, text="Password:",
      bg="lightblue").pack()

password = Entry(root, width=30, show="*")
password.pack(pady=5)

# Country
Label(root, text="Country:",
      bg="lightblue").pack()

country = StringVar(value="India")

OptionMenu(root, country,
           "India", "USA", "UK",
           "Canada", "Australia").pack(pady=5)

# Gender
Label(root, text="Gender:",
      bg="lightblue").pack()

gender = StringVar(value="Male")

Radiobutton(root, text="Male",
            variable=gender, value="Male",
            bg="lightblue").pack()

Radiobutton(root, text="Female",
            variable=gender, value="Female",
            bg="lightblue").pack()

# Submit Function
def submit():
    messagebox.showinfo(
        "Registration Successful",
        "Name: " + name.get() +
        "\nEmail: " + email.get() +
        "\nPassword: " + "*" * len(password.get()) +
        "\nCountry: " + country.get() +
        "\nGender: " + gender.get()
    )

# Submit Button
Button(root, text="SUBMIT",
       command=submit,
       bg="green", fg="white",
       font=("Arial", 12, "bold"),
       width=15).pack(pady=15)

# Clear Function
def clear():
    name.delete(0, END)
    email.delete(0, END)
    password.delete(0, END)
    phone.delete(0, END)
    country.set("India")
    gender.set("Male")

# Clear Button
Button(root, text="CLEAR",
       command=clear,
       bg="red", fg="white",
       width=15).pack()

# Run Window
root.mainloop()
