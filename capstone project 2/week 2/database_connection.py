import mysql.connector
from pymongo import MongoClient
from pymongo.errors import PyMongoError

# ==========================================
# 1. CONNECT TO MYSQL
# ==========================================

print("\n========== MYSQL CONNECTION ==========")

try:
    mysql_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password123",
        database="employee_attendance_db"
    )

    if mysql_connection.is_connected():
        print("MySQL connected successfully!")

        cursor = mysql_connection.cursor()

        # Display available tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        print("\nTables in employee_attendance_db:")

        for table in tables:
            print(table[0])

        # Read employee records
        cursor.execute("SELECT * FROM employees")
        employees = cursor.fetchall()

        print("\nEmployee records:")

        for employee in employees:
            print(employee)

        cursor.close()
        mysql_connection.close()

        print("\nMySQL connection closed.")

except mysql.connector.Error as error:
    print("MySQL connection failed:", error)


# ==========================================
# 2. CONNECT TO MONGODB
# ==========================================

print("\n========== MONGODB CONNECTION ==========")

try:
    # Default local MongoDB connection
    mongo_client = MongoClient(
        "mongodb://localhost:27017/",
        serverSelectionTimeoutMS=5000
    )

    # Verify the connection
    mongo_client.admin.command("ping")

    print("MongoDB connected successfully!")

    # Select the existing database and collection
    mongo_database = mongo_client["employee_attendance_db"]
    feedback_collection = mongo_database["task_feedback"]

    # Display collection count
    feedback_count = feedback_collection.count_documents({})

    print("\nNumber of task feedback documents:", feedback_count)

    # Display feedback documents
    print("\nTask feedback records:")

    for document in feedback_collection.find().limit(10):
        print(document)

    mongo_client.close()

    print("\nMongoDB connection closed.")

except PyMongoError as error:
    print("MongoDB connection failed:", error)