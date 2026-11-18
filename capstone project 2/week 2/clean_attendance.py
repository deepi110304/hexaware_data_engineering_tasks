import pandas as pd
# Load the original CSV files
attendance = pd.read_csv("attendance.csv")
tasks = pd.read_csv("tasks.csv")
print("Original attendance rows:", len(attendance))
print("Original task rows:", len(tasks))
# 1. Remove exact duplicate rows
attendance = attendance.drop_duplicates().copy()
tasks = tasks.drop_duplicates().copy()
# 2. Convert attendance dates and times
attendance["attendance_date"] = pd.to_datetime(
    attendance["attendance_date"], errors="coerce"
)
attendance["clock_in"] = pd.to_datetime(
    attendance["clock_in"], errors="coerce"
)
attendance["clock_out"] = pd.to_datetime(
    attendance["clock_out"], errors="coerce"
)
# 3. Standardize attendance status
attendance["status"] = (
    attendance["status"].str.strip().str.title()
)
# 4. Convert task dates and numeric columns
tasks["task_date"] = pd.to_datetime(
    tasks["task_date"], errors="coerce"
)
tasks["task_id"] = pd.to_numeric(
    tasks["task_id"], errors="coerce"
).astype("Int64")

tasks["tasks_completed"] = pd.to_numeric(
    tasks["tasks_completed"], errors="coerce"
)
# 5. Display missing values after cleaning
print("\n===== CLEANED ATTENDANCE =====")
print(attendance.head())
print("\nAttendance missing values:")
print(attendance.isnull().sum())
print("\n===== CLEANED TASKS =====")
print(tasks.head())
print("\nTask missing values:")
print(tasks.isnull().sum())
# 6. Save cleaned copies
attendance.to_csv("attendance_cleaned.csv", index=False)
tasks.to_csv("tasks_cleaned.csv", index=False)
print("\nCleaning completed successfully!")
print("Created attendance_cleaned.csv")
print("Created tasks_cleaned.csv")