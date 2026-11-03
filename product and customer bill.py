from tkinter import *
from tkinter import ttk, messagebox
from pymongo import MongoClient

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["BillingDB"]
collection = db["bills"]

# Main Window
root = Tk()
root.title("Product and Customer Bill Management")
root.geometry("1100x750")
root.configure(bg="lavender")

# Heading
Label(
    root,
    text="Product and Customer Bill Management System",
    font=("Arial", 18, "bold"),
    bg="lavender",
    fg="purple"
).pack(pady=10)

# Variables
bill_id = StringVar()
customer = StringVar()
product = StringVar()
quantity = StringVar()
price = StringVar()
discount = StringVar()

amount = StringVar()
discount_amount = StringVar()
gst = StringVar()
final_bill = StringVar()

# Form Frame
frame = Frame(root, bg="lavender")
frame.pack(pady=10)

def create_field(label, variable, row, col):
    Label(
        frame, text=label,
        font=("Arial", 11, "bold"),
        bg="lavender"
    ).grid(row=row, column=col, padx=10, pady=7)

    Entry(
        frame, textvariable=variable,
        font=("Arial", 11), width=20
    ).grid(row=row, column=col+1, padx=10, pady=7)


create_field("Bill ID", bill_id, 0, 0)
create_field("Customer Name", customer, 0, 2)

create_field("Product Name", product, 1, 0)
create_field("Quantity", quantity, 1, 2)

create_field("Price", price, 2, 0)
create_field("Discount (%)", discount, 2, 2)

create_field("Amount", amount, 3, 0)
create_field("Discount Amount", discount_amount, 3, 2)

create_field("GST (18%)", gst, 4, 0)
create_field("Final Bill", final_bill, 4, 2)


# Calculate Function
def calculate():
    try:
        q = int(quantity.get())
        p = float(price.get())
        d = float(discount.get())

        if q <= 0 or p < 0 or d < 0 or d > 100:
            messagebox.showerror(
                "Error",
                "Enter valid Quantity, Price and Discount (0-100)."
            )
            return None

        amt = q * p
        disc = amt * d / 100
        taxable = amt - disc
        tax = taxable * 18 / 100
        final = taxable + tax

        amount.set(f"{amt:.2f}")
        discount_amount.set(f"{disc:.2f}")
        gst.set(f"{tax:.2f}")
        final_bill.set(f"{final:.2f}")

        return {
            "amount": amt,
            "discount_amount": disc,
            "gst": tax,
            "final_bill": final
        }

    except ValueError:
        messagebox.showerror(
            "Error",
            "Enter valid numeric values."
        )
        return None


# Clear Function
def clear():
    bill_id.set("")
    customer.set("")
    product.set("")
    quantity.set("")
    price.set("")
    discount.set("")
    amount.set("")
    discount_amount.set("")
    gst.set("")
    final_bill.set("")


# Insert Function
def insert():
    try:
        if not bill_id.get().strip() or not customer.get().strip() or not product.get().strip():
            messagebox.showerror(
                "Error", "Please fill all required fields."
            )
            return

        if collection.find_one({"bill_id": bill_id.get().strip()}):
            messagebox.showerror(
                "Error", "Bill ID already exists."
            )
            return

        result = calculate()

        if result is None:
            return

        data = {
            "bill_id": bill_id.get().strip(),
            "customer": customer.get().strip(),
            "product": product.get().strip(),
            "quantity": int(quantity.get()),
            "price": float(price.get()),
            "discount": float(discount.get()),
            "amount": result["amount"],
            "discount_amount": result["discount_amount"],
            "gst": result["gst"],
            "final_bill": result["final_bill"]
        }

        collection.insert_one(data)

        messagebox.showinfo(
            "Success", "Bill inserted successfully!"
        )

        display()
        clear()

    except Exception as e:
        messagebox.showerror("Error", str(e))


# Update Function
def update():
    try:
        bid = bill_id.get().strip()

        if not bid:
            messagebox.showerror(
                "Error", "Enter Bill ID."
            )
            return

        result = calculate()

        if result is None:
            return

        data = {
            "customer": customer.get().strip(),
            "product": product.get().strip(),
            "quantity": int(quantity.get()),
            "price": float(price.get()),
            "discount": float(discount.get()),
            "amount": result["amount"],
            "discount_amount": result["discount_amount"],
            "gst": result["gst"],
            "final_bill": result["final_bill"]
        }

        res = collection.update_one(
            {"bill_id": bid},
            {"$set": data}
        )

        if res.matched_count > 0:
            messagebox.showinfo(
                "Success", "Bill updated successfully!"
            )
            display()
            clear()
        else:
            messagebox.showerror(
                "Error", "Bill ID not found."
            )

    except Exception as e:
        messagebox.showerror("Error", str(e))


# Delete Function
def delete():
    bid = bill_id.get().strip()

    if not bid:
        messagebox.showerror(
            "Error", "Enter Bill ID."
        )
        return

    confirm = messagebox.askyesno(
        "Confirm", "Do you want to delete this bill?"
    )

    if confirm:
        res = collection.delete_one({"bill_id": bid})

        if res.deleted_count > 0:
            messagebox.showinfo(
                "Success", "Bill deleted successfully!"
            )
            display()
            clear()
        else:
            messagebox.showerror(
                "Error", "Bill ID not found."
            )


# Search Function
def search():
    bid = bill_id.get().strip()
    name = customer.get().strip()

    if bid:
        data = collection.find_one({"bill_id": bid})
    elif name:
        data = collection.find_one({
            "customer": {
                "$regex": "^" + name + "$",
                "$options": "i"
            }
        })
    else:
        messagebox.showerror(
            "Error", "Enter Bill ID or Customer Name."
        )
        return

    if data:
        clear()

        bill_id.set(data["bill_id"])
        customer.set(data["customer"])
        product.set(data["product"])
        quantity.set(str(data["quantity"]))
        price.set(str(data["price"]))
        discount.set(str(data["discount"]))

        amount.set(str(data["amount"]))
        discount_amount.set(str(data["discount_amount"]))
        gst.set(str(data["gst"]))
        final_bill.set(str(data["final_bill"]))

    else:
        messagebox.showerror(
            "Error", "Bill not found."
        )


# Display Function
def display():
    for row in tree.get_children():
        tree.delete(row)

    for data in collection.find():
        tree.insert("", END, values=(
            data["bill_id"],
            data["customer"],
            data["product"],
            data["quantity"],
            data["price"],
            data["amount"],
            data["discount_amount"],
            data["gst"],
            data["final_bill"]
        ))


# Select Table Record
def select_record(event):
    selected = tree.focus()

    if selected:
        values = tree.item(selected, "values")

        clear()

        bill_id.set(values[0])
        customer.set(values[1])
        product.set(values[2])
        quantity.set(values[3])
        price.set(values[4])

        data = collection.find_one({"bill_id": values[0]})

        if data:
            discount.set(str(data["discount"]))
            amount.set(str(data["amount"]))
            discount_amount.set(str(data["discount_amount"]))
            gst.set(str(data["gst"]))
            final_bill.set(str(data["final_bill"]))


# Buttons Frame
button_frame = Frame(root, bg="lavender")
button_frame.pack(pady=10)

buttons = [
    ("CALCULATE", calculate),
    ("INSERT", insert),
    ("UPDATE", update),
    ("DELETE", delete),
    ("SEARCH", search),
    ("CLEAR", clear),
    ("EXIT", root.destroy)
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
    "Bill ID", "Customer", "Product",
    "Quantity", "Price", "Amount",
    "Discount", "GST", "Final Bill"
)

tree = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=110, anchor=CENTER)

tree.pack(fill=BOTH, expand=True)

tree.bind("<<TreeviewSelect>>", select_record)


# Close MongoDB Connection
def exit_app():
    client.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", exit_app)

# Run Application
root.mainloop()
