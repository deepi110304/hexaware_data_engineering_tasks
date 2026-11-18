import json
import mysql.connector
from pymongo import MongoClient
from bson import json_util


# ==========================================
# 1. MYSQL CONNECTION
# ==========================================

print("\n========== MYSQL DATA EXPORT ==========")

mysql_connection = None

try:
    mysql_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password123",
        database="employee_attendance_db"
    )

    print("Connected to MySQL successfully!")

    # Export each MySQL table
    tables = ["employees", "attendance", "tasks"]

    for table_name in tables:

        query = f"SELECT * FROM `{table_name}`"

        cursor = mysql_connection.cursor()
        cursor.execute(query)

        records = cursor.fetchall()
        columns = [column[0] for column in cursor.description]

        import pandas as pd

        dataframe = pd.DataFrame(
            records,
            columns=columns
        )

        output_file = f"{table_name}_from_mysql.csv"

        dataframe.to_csv(
            output_file,
            index=False
        )

        print(
            f"{table_name}: {len(dataframe)} records exported "
            f"to {output_file}"
        )

        cursor.close()

except mysql.connector.Error as error:
    print("MySQL error:", error)

finally:
    if mysql_connection and mysql_connection.is_connected():
        mysql_connection.close()
        print("MySQL connection closed.")


# ==========================================
# 2. MONGODB CONNECTION
# ==========================================

print("\n========== MONGODB DATA EXPORT ==========")

mongo_client = None

try:
    mongo_client = MongoClient(
        "mongodb://localhost:27017/",
        serverSelectionTimeoutMS=5000
    )

    mongo_client.admin.command("ping")

    print("Connected to MongoDB successfully!")

    database = mongo_client["employee_attendance_db"]
    collection = database["task_feedback"]

    feedback_documents = list(collection.find())

    # Convert MongoDB documents to Extended JSON.
    # This preserves MongoDB-specific types such as ObjectId.
    with open(
        "task_feedback_from_mongodb.json",
        "w",
        encoding="utf-8"
    ) as json_file:

        json_file.write(
            json_util.dumps(
                feedback_documents,
                indent=4
            )
        )

    print(
        f"{len(feedback_documents)} feedback documents exported "
        "to task_feedback_from_mongodb.json"
    )

except Exception as error:
    print("MongoDB error:", error)

finally:
    if mongo_client is not None:
        mongo_client.close()
        print("MongoDB connection closed.")


print("\nDatabase export process finished.")