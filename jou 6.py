'''jounal 6
1.Environment Setup and Database/Collection Initialization:
1. Connect to MongoDB 
2. Select Database and Collection 
2.Data Insertion (Create Operations):
1. Insert Sample Student Documents 
2. Vary your data 
3.Data Retrieval (Read Operations):
1. Basic Retrieval 
2. Filtered Retrieval 
3. Advanced Retrieval (using sort, limit, skip) 4. Aggregation Queries: Count Students per Major, Average Marks per Course, Students 
with High Marks in a Course 
4.Data Update (Update Operations):
1. Update Top-Level Field 
2. Add a New Enrollment 
3. Update Embedded Field (Specific Array Element) 
4. Remove an Enrollment 
5. Upsert Operation 
5.Data Deletion (Delete Operations):
1. Delete a Single Student 
2. Delete Multiple Students 
6.Data Export and Import (External Files):
1. Export Data to JSON 
2. Import Data from JSON
'''
from pymongo import MongoClient, ASCENDING, DESCENDING
import json

# ==========================================
# 1. ENVIRONMENT SETUP AND DATABASE
# ==========================================

client = MongoClient("mongodb://localhost:27017/")

db = client["university"]
students = db["students"]

print("\nConnected to MongoDB Successfully!")


# ==========================================
# 2. DATA INSERTION (CREATE)
# ==========================================

sample_students = [
    {
        "student_id": 101,
        "name": "Rahul",
        "age": 20,
        "major": "Computer Science",
        "marks": 85,
        "enrollments": [
            {"course": "Python", "marks": 90},
            {"course": "Java", "marks": 80}
        ]
    },
    {
        "student_id": 102,
        "name": "Priya",
        "age": 21,
        "major": "IT",
        "marks": 92,
        "enrollments": [
            {"course": "Python", "marks": 95},
            {"course": "Database", "marks": 89}
        ]
    },
    {
        "student_id": 103,
        "name": "Amit",
        "age": 20,
        "major": "Computer Science",
        "marks": 75,
        "enrollments": [
            {"course": "Java", "marks": 70},
            {"course": "Database", "marks": 80}
        ]
    },
    {
        "student_id": 104,
        "name": "Neha",
        "age": 22,
        "major": "IT",
        "marks": 88,
        "enrollments": [
            {"course": "Python", "marks": 85}
        ]
    }
]

# Insert sample data only if collection is empty
if students.count_documents({}) == 0:
    students.insert_many(sample_students)
    print("\nStudent Records Inserted Successfully!")


# ==========================================
# 3. DATA RETRIEVAL (READ)
# ==========================================

print("\n--- 1. BASIC RETRIEVAL ---")

for student in students.find():
    print(student)


# Filtered Retrieval
print("\n--- 2. FILTERED RETRIEVAL ---")

for student in students.find({"major": "IT"}):
    print(student)


# Advanced Retrieval (Sort, Limit, Skip)
print("\n--- 3. ADVANCED RETRIEVAL ---")

for student in students.find().sort(
    "marks", DESCENDING
).limit(2).skip(0):
    print(student)


# ==========================================
# 4. AGGREGATION QUERIES
# ==========================================

# Count Students per Major
print("\n--- STUDENTS PER MAJOR ---")

pipeline = [
    {
        "$group": {
            "_id": "$major",
            "total_students": {"$sum": 1}
        }
    }
]

for result in students.aggregate(pipeline):
    print(result)


# Average Marks per Course
print("\n--- AVERAGE MARKS PER COURSE ---")

pipeline = [
    {"$unwind": "$enrollments"},
    {
        "$group": {
            "_id": "$enrollments.course",
            "average_marks": {
                "$avg": "$enrollments.marks"
            }
        }
    }
]

for result in students.aggregate(pipeline):
    print(result)


# Students with High Marks in a Course
print("\n--- STUDENTS WITH HIGH MARKS ---")

pipeline = [
    {"$unwind": "$enrollments"},
    {
        "$match": {
            "enrollments.marks": {"$gte": 85}
        }
    },
    {
        "$project": {
            "_id": 0,
            "name": 1,
            "course": "$enrollments.course",
            "marks": "$enrollments.marks"
        }
    }
]

for result in students.aggregate(pipeline):
    print(result)


# ==========================================
# 5. DATA UPDATE (UPDATE)
# ==========================================

# Update Top-Level Field
print("\n--- UPDATE TOP LEVEL FIELD ---")

students.update_one(
    {"student_id": 101},
    {"$set": {"age": 21}}
)

print("Age Updated Successfully!")


# Add a New Enrollment
print("\n--- ADD NEW ENROLLMENT ---")

students.update_one(
    {"student_id": 101},
    {
        "$push": {
            "enrollments": {
                "course": "Machine Learning",
                "marks": 90
            }
        }
    }
)

print("New Enrollment Added!")


# Update Embedded Field (Specific Array Element)
print("\n--- UPDATE EMBEDDED FIELD ---")

students.update_one(
    {
        "student_id": 101,
        "enrollments.course": "Python"
    },
    {
        "$set": {
            "enrollments.$.marks": 95
        }
    }
)

print("Embedded Marks Updated!")


# Remove an Enrollment
print("\n--- REMOVE ENROLLMENT ---")

students.update_one(
    {"student_id": 101},
    {
        "$pull": {
            "enrollments": {
                "course": "Java"
            }
        }
    }
)

print("Enrollment Removed!")


# Upsert Operation
print("\n--- UPSERT OPERATION ---")

students.update_one(
    {"student_id": 105},
    {
        "$set": {
            "name": "Karan",
            "age": 21,
            "major": "IT",
            "marks": 80,
            "enrollments": []
        }
    },
    upsert=True
)

print("Upsert Operation Completed!")


# ==========================================
# 6. DATA DELETION (DELETE)
# ==========================================

# Delete Single Student
print("\n--- DELETE SINGLE STUDENT ---")

students.delete_one({"student_id": 104})

print("Single Student Deleted!")


# Delete Multiple Students
print("\n--- DELETE MULTIPLE STUDENTS ---")

students.delete_many({"marks": {"$lt": 80}})

print("Multiple Students Deleted!")


# ==========================================
# 7. DATA EXPORT TO JSON
# ==========================================

print("\n--- EXPORT DATA TO JSON ---")

data = list(students.find({}, {"_id": 0}))

with open("students.json", "w") as file:
    json.dump(data, file, indent=4)

print("Data Exported to students.json Successfully!")


# ==========================================
# 8. DATA IMPORT FROM JSON
# ==========================================

print("\n--- IMPORT DATA FROM JSON ---")

with open("students.json", "r") as file:
    imported_data = json.load(file)

if imported_data:
    students.insert_many(imported_data)

print("Data Imported Successfully!")


# ==========================================
# FINAL DISPLAY
# ==========================================

print("\n--- FINAL STUDENT RECORDS ---")

for student in students.find():
    print(student)


# Close Connection
client.close()

print("\nMongoDB Connection Closed!")
