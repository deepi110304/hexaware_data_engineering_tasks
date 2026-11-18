
import pandas as pd
import numpy as np

# Load the CSV files
attendance = pd.read_csv("attendance.csv")
tasks = pd.read_csv("tasks.csv")
employees = pd.read_csv("employee.csv")

# Display attendance data
print("===== ATTENDANCE DATA =====")
print(attendance.head())
print("Attendance shape:", attendance.shape)

# Display task data
print("\n===== TASK DATA =====")
print(tasks.head())
print("Tasks shape:", tasks.shape)

# Display employee data
print("\n===== EMPLOYEE DATA =====")
print(employees.head())
print("Employees shape:", employees.shape)

# Check missing values
print("\n===== MISSING VALUES =====")
print("Attendance:\n", attendance.isnull().sum())
print("Tasks:\n", tasks.isnull().sum())
print("Employees:\n", employees.isnull().sum())

# Check column data types
print("\n===== DATA TYPES =====")
print("Attendance:\n", attendance.dtypes)
print("Tasks:\n", tasks.dtypes)