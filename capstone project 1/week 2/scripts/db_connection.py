
import mysql.connector
from pymongo import MongoClient

# MySQL settings — use your actual database details
MYSQL_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "password123",
    "database": "retail_sales_db"
}

# MongoDB settings
MONGO_URI = "mongodb://localhost:27017/"
MONGO_DATABASE = "retail_sales_db"


def test_mysql_connection():
    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        print("MySQL connected successfully!")

        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")

        print("\nMySQL tables:")
        tables = cursor.fetchall()

        if tables:
            for table in tables:
                print("-", table[0])
        else:
            print("No tables found in this database.")

    except mysql.connector.Error as error:
        print("MySQL error:", error)

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def test_mongodb_connection():
    client = None

    try:
        client = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=5000
        )

        client.admin.command("ping")
        print("\nMongoDB connected successfully!")

        database = client[MONGO_DATABASE]
        collections = database.list_collection_names()

        print("MongoDB collections:")
        if collections:
            for collection in collections:
                print("-", collection)
        else:
            print("No collections found in this database.")

    except Exception as error:
        print("MongoDB error:", error)

    finally:
        if client:
            client.close()


if __name__ == "__main__":
    test_mysql_connection()
    test_mongodb_connection()