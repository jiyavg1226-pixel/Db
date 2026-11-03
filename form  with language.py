from tkinter import *
from tkinter import messagebox

# Main Window
root = Tk()
root.title("Registration Form")
root.geometry("450x550")
root.configure(bg="ivory")

# Heading
Label(root, text="REGISTRATION FORM",
      font=("Arial", 20, "bold"),
      bg="ivory", fg="darkblue").pack(pady=20)

# Name
Label(root, text="Name:",
      bg="ivory", fg="black").pack()

name = Entry(root, width=30)
name.pack(pady=5)

# Email
Label(root, text="Email:",
      bg="ivory").pack()

email = Entry(root, width=30)
email.pack(pady=5)

# Password
Label(root, text="Password:",
      bg="ivory").pack()

password = Entry(root, width=30, show="*")
password.pack(pady=5)

# Language Selection
Label(root, text="Select Language:",
      bg="ivory").pack()

language = StringVar(value="English")

Checkbutton(root, text="English",
            variable=StringVar(value=0),
            bg="ivory").pack()

lang1 = IntVar()
lang2 = IntVar()
lang3 = IntVar()

Checkbutton(root, text="Gujarati",
            variable=lang1,
            bg="ivory").pack()

Checkbutton(root, text="Hindi",
            variable=lang2,
            bg="ivory").pack()

Checkbutton(root, text="English",
            variable=lang3,
            bg="ivory").pack()

# Submit Function
def submit():
    selected = []

    if lang1.get():
        selected.append("Gujarati")

    if lang2.get():
        selected.append("Hindi")

    if lang3.get():
        selected.append("English")

    messagebox.showinfo(
        "Registration Successful",
        "Name: " + name.get() +
        "\nEmail: " + email.get() +
        "\nPassword: " + "*" * len(password.get()) +
        "\nLanguages: " + ", ".join(selected)
    )

# Submit Button
Button(root, text="SUBMIT",
       command=submit,
       bg="darkgreen", fg="white",
       font=("Arial", 12, "bold"),
       width=15).pack(pady=15)

# Clear Function
def clear():
    name.delete(0, END)
    email.delete(0, END)
    phone.delete(0, END)
    password.delete(0, END)
    lang1.set(0)
    lang2.set(0)
    lang3.set(0)

# Clear Button
Button(root, text="CLEAR",
       command=clear,
       bg="darkred", fg="white",
       width=15).pack()

# Run Application
root.mainloop()
