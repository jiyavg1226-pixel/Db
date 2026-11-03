import sqlite3

# 1. DATABASE CONNECTION
conn = sqlite3.connect("todo.db")
cursor = conn.cursor()

print("Database Connected Successfully!")

# CREATE TASKS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    due_date TEXT,
    completed INTEGER DEFAULT 0
)
""")

conn.commit()
print("Tasks Table Created Successfully!")


# 2. ADD TASK FUNCTION
def add_task(description, due_date):
    cursor.execute("""
    INSERT INTO tasks (description, due_date)
    VALUES (?, ?)
    """, (description, due_date))

    conn.commit()
    print("Task Added Successfully!")


# VIEW TASKS FUNCTION
def view_tasks(show_completed=False):

    if show_completed:
        cursor.execute("SELECT * FROM tasks")
    else:
        cursor.execute("SELECT * FROM tasks WHERE completed = 0")

    tasks = cursor.fetchall()

    if not tasks:
        print("No Tasks Found!")
    else:
        print("\n--- TO-DO LIST ---")

        for task in tasks:
            status = "Completed" if task[3] else "Pending"

            print("ID:", task[0])
            print("Description:", task[1])
            print("Due Date:", task[2])
            print("Status:", status)
            print("-------------------")


# 4 MARK TASK COMPLETED FUNCTION
def mark_task_completed(task_id):

    cursor.execute("""
    UPDATE tasks
    SET completed = 1
    WHERE task_id = ?
    """, (task_id,))

    conn.commit()

    if cursor.rowcount > 0:
        print("Task Marked as Completed!")
    else:
        print("Task ID Not Found!")


# DELETE TASK FUNCTION
def delete_task(task_id):

    cursor.execute("""
    DELETE FROM tasks
    WHERE task_id = ?
    """, (task_id,))

    conn.commit()

    if cursor.rowcount > 0:
        print("Task Deleted Successfully!")
    else:
        print("Task ID Not Found!")


# 6. MAIN PROGRAM LOOP
while True:

    print("\n===== TO-DO LIST MANAGER =====")
    print("1. Add New Task")
    print("2. View Pending Tasks")
    print("3. View All Tasks")
    print("4. Mark Task as Completed")
    print("5. Delete Task")
    print("6. Exit")

    try:
        choice = int(input("Enter Your Choice: "))

        if choice == 1:

            description = input("Enter Task Description: ")
            due_date = input("Enter Due Date (YYYY-MM-DD): ")

            add_task(description, due_date)

        elif choice == 2:

            view_tasks(False)

        elif choice == 3:

            view_tasks(True)

        elif choice == 4:

            task_id = int(input("Enter Task ID: "))
            mark_task_completed(task_id)

        elif choice == 5:

            task_id = int(input("Enter Task ID to Delete: "))
            delete_task(task_id)

        elif choice == 6:

            print("Thank You! Exiting To-Do List Manager.")
            break

        else:
            print("Invalid Choice! Please Enter 1 to 6.")

    except ValueError:
        print("Invalid Input! Please Enter a Number.")

# CLOSE DATABASE CONNECTION
conn.close()
