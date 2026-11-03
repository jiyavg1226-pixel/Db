from tkinter import *
from tkinter import ttk, messagebox
from pymongo import MongoClient

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")

db = client["LibraryDB"]
collection = db["books"]

# Main Window
root = Tk()
root.title("Library Management System")
root.geometry("950x650")
root.configure(bg="lavender")


# Clear Fields
def clear_fields():
    book_id_entry.delete(0, END)
    title_entry.delete(0, END)
    author_entry.delete(0, END)
    publisher_entry.delete(0, END)
    price_entry.delete(0, END)
    quantity_entry.delete(0, END)


# Insert Book
def insert_book():

    book_id = book_id_entry.get()
    title = title_entry.get()
    author = author_entry.get()
    publisher = publisher_entry.get()
    price = price_entry.get()
    quantity = quantity_entry.get()

    if book_id == "" or title == "" or author == "" or publisher == "" or price == "" or quantity == "":
        messagebox.showwarning("Warning", "Please fill all fields")
        return

    try:
        price = float(price)
        quantity = int(quantity)

        if price < 0 or quantity < 0:
            messagebox.showwarning("Warning", "Enter valid price and quantity")
            return

    except ValueError:
        messagebox.showwarning("Warning", "Enter valid price and quantity")
        return

    # Check Duplicate Book ID
    if collection.find_one({"book_id": book_id}):
        messagebox.showerror("Error", "Book ID Already Exists")
        return

    data = {
        "book_id": book_id,
        "title": title,
        "author": author,
        "publisher": publisher,
        "price": price,
        "quantity": quantity
    }

    collection.insert_one(data)

    messagebox.showinfo("Success", "Book Added Successfully")

    clear_fields()
    display_books()


# Search Book
def search_book():

    book_id = book_id_entry.get()
    title = title_entry.get()

    if book_id != "":
        data = collection.find_one({"book_id": book_id})

    elif title != "":
        data = collection.find_one({
            "title": {"$regex": "^" + title + "$", "$options": "i"}
        })

    else:
        messagebox.showwarning("Warning", "Enter Book ID or Book Title")
        return

    if data:

        clear_fields()

        book_id_entry.insert(0, data["book_id"])
        title_entry.insert(0, data["title"])
        author_entry.insert(0, data["author"])
        publisher_entry.insert(0, data["publisher"])
        price_entry.insert(0, data["price"])
        quantity_entry.insert(0, data["quantity"])

        messagebox.showinfo("Success", "Book Found")

    else:
        messagebox.showerror("Error", "Book Not Found")


# Update Book
def update_book():

    book_id = book_id_entry.get()

    if book_id == "":
        messagebox.showwarning("Warning", "Enter Book ID")
        return

    data = collection.find_one({"book_id": book_id})

    if data is None:
        messagebox.showerror("Error", "Book Not Found")
        return

    title = title_entry.get()
    author = author_entry.get()
    publisher = publisher_entry.get()
    price = price_entry.get()
    quantity = quantity_entry.get()

    if title == "" or author == "" or publisher == "" or price == "" or quantity == "":
        messagebox.showwarning("Warning", "Please fill all fields")
        return

    try:
        price = float(price)
        quantity = int(quantity)

        if price < 0 or quantity < 0:
            messagebox.showwarning("Warning", "Enter valid price and quantity")
            return

    except ValueError:
        messagebox.showwarning("Warning", "Enter valid price and quantity")
        return

    collection.update_one(
        {"book_id": book_id},
        {"$set": {
            "title": title,
            "author": author,
            "publisher": publisher,
            "price": price,
            "quantity": quantity
        }}
    )

    messagebox.showinfo("Success", "Book Updated Successfully")

    clear_fields()
    display_books()


# Delete Book
def delete_book():

    book_id = book_id_entry.get()

    if book_id == "":
        messagebox.showwarning("Warning", "Enter Book ID")
        return

    data = collection.find_one({"book_id": book_id})

    if data is None:
        messagebox.showerror("Error", "Book Not Found")
        return

    answer = messagebox.askyesno(
        "Confirm",
        "Are you sure you want to delete this book?"
    )

    if answer:
        collection.delete_one({"book_id": book_id})

        messagebox.showinfo("Success", "Book Deleted Successfully")

        clear_fields()
        display_books()


# Display All Books
def display_books():

    for row in tree.get_children():
        tree.delete(row)

    records = collection.find()

    for data in records:
        tree.insert("", END, values=(
            data["book_id"],
            data["title"],
            data["author"],
            data["publisher"],
            data["price"],
            data["quantity"]
        ))


# Select Book from Table
def select_book(event):

    selected = tree.focus()

    if selected == "":
        return

    values = tree.item(selected, "values")

    clear_fields()

    book_id_entry.insert(0, values[0])
    title_entry.insert(0, values[1])
    author_entry.insert(0, values[2])
    publisher_entry.insert(0, values[3])
    price_entry.insert(0, values[4])
    quantity_entry.insert(0, values[5])


# Heading
Label(
    root,
    text="LIBRARY MANAGEMENT SYSTEM",
    font=("Arial", 22, "bold"),
    bg="lavender",
    fg="purple"
).pack(pady=15)


# Form Frame
form = Frame(root, bg="lavender")
form.pack(pady=10)


# Book ID
Label(form, text="Book ID:", bg="lavender",
      font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=8)

book_id_entry = Entry(form, width=25, font=("Arial", 12))
book_id_entry.grid(row=0, column=1)


# Book Title
Label(form, text="Book Title:", bg="lavender",
      font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=8)

title_entry = Entry(form, width=25, font=("Arial", 12))
title_entry.grid(row=1, column=1)


# Author
Label(form, text="Author:", bg="lavender",
      font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=8)

author_entry = Entry(form, width=25, font=("Arial", 12))
author_entry.grid(row=2, column=1)


# Publisher
Label(form, text="Publisher:", bg="lavender",
      font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=8)

publisher_entry = Entry(form, width=25, font=("Arial", 12))
publisher_entry.grid(row=3, column=1)


# Price
Label(form, text="Price:", bg="lavender",
      font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=8)

price_entry = Entry(form, width=25, font=("Arial", 12))
price_entry.grid(row=4, column=1)


# Quantity
Label(form, text="Quantity:", bg="lavender",
      font=("Arial", 12)).grid(row=5, column=0, padx=10, pady=8)

quantity_entry = Entry(form, width=25, font=("Arial", 12))
quantity_entry.grid(row=5, column=1)


# Buttons
button_frame = Frame(root, bg="lavender")
button_frame.pack(pady=15)

Button(button_frame, text="INSERT", width=13,
       bg="plum", command=insert_book).grid(row=0, column=0, padx=5, pady=5)

Button(button_frame, text="UPDATE", width=13,
       bg="plum", command=update_book).grid(row=0, column=1, padx=5, pady=5)

Button(button_frame, text="DELETE", width=13,
       bg="plum", command=delete_book).grid(row=0, column=2, padx=5, pady=5)

Button(button_frame, text="SEARCH", width=13,
       bg="plum", command=search_book).grid(row=0, column=3, padx=5, pady=5)


Button(button_frame, text="CLEAR", width=13,
       bg="plum", command=clear_fields).grid(row=0, column=5, padx=5, pady=5)


# Book Records Table
tree = ttk.Treeview(
    root,
    columns=("ID", "Title", "Author", "Publisher", "Price", "Quantity"),
    show="headings"
)

tree.heading("ID", text="Book ID")
tree.heading("Title", text="Book Title")
tree.heading("Author", text="Author")
tree.heading("Publisher", text="Publisher")
tree.heading("Price", text="Price")
tree.heading("Quantity", text="Quantity")

tree.column("ID", width=90)
tree.column("Title", width=150)
tree.column("Author", width=130)
tree.column("Publisher", width=130)
tree.column("Price", width=90)
tree.column("Quantity", width=90)

tree.pack(pady=15, fill=X, padx=15)

# Select Row Event
tree.bind("<<TreeviewSelect>>", select_book)

# Display Existing Records
display_books()


# Close Application
def close_app():
    client.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", close_app)

# Run Application
root.mainloop()
