from tkinter import *
from tkinter import ttk, messagebox
from pymongo import MongoClient

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")

db = client["BankDB"]
collection = db["accounts"]

# Main Window
root = Tk()
root.title("Bank Account Management System")
root.geometry("1000x700")
root.configure(bg="lavender")

selected_id = None


# Clear Fields
def clear_fields():
    global selected_id
    selected_id = None

    id_entry.delete(0, END)
    name_entry.delete(0, END)
    account_entry.delete(0, END)
    phone_entry.delete(0, END)
    balance_entry.delete(0, END)


# Create Account
def create_account():

    account_id = id_entry.get()
    name = name_entry.get()
    account_type = account_entry.get()
    phone = phone_entry.get()
    balance = balance_entry.get()

    if account_id == "" or name == "" or account_type == "" or phone == "" or balance == "":
        messagebox.showwarning("Warning", "Please fill all fields")
        return

    try:
        balance = float(balance)

        if balance < 0:
            messagebox.showwarning("Warning", "Balance cannot be negative")
            return

    except ValueError:
        messagebox.showwarning("Warning", "Enter valid balance")
        return

    # Check Duplicate Account
    if collection.find_one({"account_id": account_id}):
        messagebox.showerror("Error", "Account ID Already Exists")
        return

    data = {
        "account_id": account_id,
        "name": name,
        "account_type": account_type,
        "phone": phone,
        "balance": balance
    }

    collection.insert_one(data)

    messagebox.showinfo("Success", "Account Created Successfully")

    clear_fields()
    display_accounts()


# Search Account
def search_account():

    account_id = id_entry.get()
    name = name_entry.get()

    if account_id != "":
        data = collection.find_one({"account_id": account_id})

    elif name != "":
        data = collection.find_one({
            "name": {"$regex": "^" + name + "$", "$options": "i"}
        })

    else:
        messagebox.showwarning("Warning", "Enter Account ID or Name")
        return

    if data:

        clear_fields()

        id_entry.insert(0, data["account_id"])
        name_entry.insert(0, data["name"])
        account_entry.insert(0, data["account_type"])
        phone_entry.insert(0, data["phone"])
        balance_entry.insert(0, str(data["balance"]))

        messagebox.showinfo("Success", "Account Found")

    else:
        messagebox.showerror("Error", "Account Not Found")


# Deposit Money
def deposit_money():

    account_id = id_entry.get()

    if account_id == "":
        messagebox.showwarning("Warning", "Enter Account ID")
        return

    data = collection.find_one({"account_id": account_id})

    if data is None:
        messagebox.showerror("Error", "Account Not Found")
        return

    try:
        amount = float(deposit_entry.get())

        if amount <= 0:
            messagebox.showwarning("Warning", "Enter valid deposit amount")
            return

    except ValueError:
        messagebox.showwarning("Warning", "Enter valid amount")
        return

    new_balance = data["balance"] + amount

    collection.update_one(
        {"account_id": account_id},
        {"$set": {"balance": new_balance}}
    )

    balance_entry.delete(0, END)
    balance_entry.insert(0, str(new_balance))

    messagebox.showinfo("Success", "Money Deposited Successfully")

    deposit_entry.delete(0, END)
    display_accounts()


# Withdraw Money
def withdraw_money():

    account_id = id_entry.get()

    if account_id == "":
        messagebox.showwarning("Warning", "Enter Account ID")
        return

    data = collection.find_one({"account_id": account_id})

    if data is None:
        messagebox.showerror("Error", "Account Not Found")
        return

    try:
        amount = float(deposit_entry.get())

        if amount <= 0:
            messagebox.showwarning("Warning", "Enter valid withdrawal amount")
            return

    except ValueError:
        messagebox.showwarning("Warning", "Enter valid amount")
        return

    if amount > data["balance"]:
        messagebox.showerror("Error", "Insufficient Balance")
        return

    new_balance = data["balance"] - amount

    collection.update_one(
        {"account_id": account_id},
        {"$set": {"balance": new_balance}}
    )

    balance_entry.delete(0, END)
    balance_entry.insert(0, str(new_balance))

    messagebox.showinfo("Success", "Money Withdrawn Successfully")

    deposit_entry.delete(0, END)
    display_accounts()


# Display Balance
def display_balance():

    account_id = id_entry.get()

    if account_id == "":
        messagebox.showwarning("Warning", "Enter Account ID")
        return

    data = collection.find_one({"account_id": account_id})

    if data:
        balance_entry.delete(0, END)
        balance_entry.insert(0, str(data["balance"]))

        messagebox.showinfo(
            "Account Balance",
            f"Current Balance: ₹{data['balance']:.2f}"
        )

    else:
        messagebox.showerror("Error", "Account Not Found")


# Update Account
def update_account():

    account_id = id_entry.get()

    if account_id == "":
        messagebox.showwarning("Warning", "Enter Account ID")
        return

    data = collection.find_one({"account_id": account_id})

    if data is None:
        messagebox.showerror("Error", "Account Not Found")
        return

    name = name_entry.get()
    account_type = account_entry.get()
    phone = phone_entry.get()

    if name == "" or account_type == "" or phone == "":
        messagebox.showwarning("Warning", "Fill all account details")
        return

    collection.update_one(
        {"account_id": account_id},
        {"$set": {
            "name": name,
            "account_type": account_type,
            "phone": phone
        }}
    )

    messagebox.showinfo("Success", "Account Updated Successfully")

    display_accounts()


# Delete Account
def delete_account():

    account_id = id_entry.get()

    if account_id == "":
        messagebox.showwarning("Warning", "Enter Account ID")
        return

    data = collection.find_one({"account_id": account_id})

    if data is None:
        messagebox.showerror("Error", "Account Not Found")
        return

    answer = messagebox.askyesno(
        "Confirm",
        "Are you sure you want to delete this account?"
    )

    if answer:
        collection.delete_one({"account_id": account_id})

        messagebox.showinfo("Success", "Account Deleted Successfully")

        clear_fields()
        display_accounts()


# Display All Accounts
def display_accounts():

    for row in tree.get_children():
        tree.delete(row)

    records = collection.find()

    for data in records:
        tree.insert("", END, values=(
            data["account_id"],
            data["name"],
            data["account_type"],
            data["phone"],
            data["balance"]
        ))


# Select Account from Table
def select_account(event):

    selected = tree.focus()

    if selected == "":
        return

    values = tree.item(selected, "values")

    clear_fields()

    id_entry.insert(0, values[0])
    name_entry.insert(0, values[1])
    account_entry.insert(0, values[2])
    phone_entry.insert(0, values[3])
    balance_entry.insert(0, values[4])


# Heading
Label(
    root,
    text="BANK ACCOUNT MANAGEMENT SYSTEM",
    font=("Arial", 22, "bold"),
    bg="lavender",
    fg="purple"
).pack(pady=15)


# Form Frame
form = Frame(root, bg="lavender")
form.pack(pady=10)


# Account ID
Label(form, text="Account ID:", bg="lavender",
      font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=8)

id_entry = Entry(form, width=25, font=("Arial", 12))
id_entry.grid(row=0, column=1)


# Account Holder Name
Label(form, text="Account Holder Name:", bg="lavender",
      font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=8)

name_entry = Entry(form, width=25, font=("Arial", 12))
name_entry.grid(row=1, column=1)


# Account Type
Label(form, text="Account Type:", bg="lavender",
      font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=8)

account_entry = ttk.Combobox(
    form,
    values=["Savings", "Current"],
    width=23,
    state="readonly"
)
account_entry.grid(row=2, column=1)


# Phone
Label(form, text="Phone:", bg="lavender",
      font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=8)

phone_entry = Entry(form, width=25, font=("Arial", 12))
phone_entry.grid(row=3, column=1)


# Balance
Label(form, text="Balance:", bg="lavender",
      font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=8)

balance_entry = Entry(form, width=25, font=("Arial", 12))
balance_entry.grid(row=4, column=1)


# Deposit / Withdraw Amount
Label(form, text="Deposit / Withdraw Amount:", bg="lavender",
      font=("Arial", 12)).grid(row=5, column=0, padx=10, pady=8)

deposit_entry = Entry(form, width=25, font=("Arial", 12))
deposit_entry.grid(row=5, column=1)


# Buttons
button_frame = Frame(root, bg="lavender")
button_frame.pack(pady=15)

Button(button_frame, text="CREATE", width=13,
       bg="plum", command=create_account).grid(row=0, column=0, padx=5, pady=5)

Button(button_frame, text="SEARCH", width=13,
       bg="plum", command=search_account).grid(row=0, column=1, padx=5, pady=5)

Button(button_frame, text="DEPOSIT", width=13,
       bg="plum", command=deposit_money).grid(row=0, column=2, padx=5, pady=5)

Button(button_frame, text="WITHDRAW", width=13,
       bg="plum", command=withdraw_money).grid(row=0, column=3, padx=5, pady=5)

Button(button_frame, text="BALANCE", width=13,
       bg="plum", command=display_balance).grid(row=0, column=4, padx=5, pady=5)

Button(button_frame, text="UPDATE", width=13,
       bg="plum", command=update_account).grid(row=1, column=0, padx=5, pady=5)

Button(button_frame, text="DELETE", width=13,
       bg="plum", command=delete_account).grid(row=1, column=1, padx=5, pady=5)

Button(button_frame, text="DISPLAY ALL", width=13,
       bg="plum", command=display_accounts).grid(row=1, column=2, padx=5, pady=5)

Button(button_frame, text="CLEAR", width=13,
       bg="plum", command=clear_fields).grid(row=1, column=3, padx=5, pady=5)


# Account Table
tree = ttk.Treeview(
    root,
    columns=("ID", "Name", "Type", "Phone", "Balance"),
    show="headings"
)

tree.heading("ID", text="Account ID")
tree.heading("Name", text="Account Holder")
tree.heading("Type", text="Account Type")
tree.heading("Phone", text="Phone")
tree.heading("Balance", text="Balance")

tree.column("ID", width=120)
tree.column("Name", width=180)
tree.column("Type", width=120)
tree.column("Phone", width=130)
tree.column("Balance", width=120)

tree.pack(pady=15, fill=X, padx=15)

tree.bind("<<TreeviewSelect>>", select_account)

# Display Records
display_accounts()


# Close Application
def close_app():
    client.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", close_app)

# Run Application
root.mainloop()
