import pandas as pd
import random
from datetime import datetime, timedelta

random.seed(42)

# Load employee details
employees = pd.read_csv("employee.csv")

# Keep only employee information if these columns exist
employee_columns = [
    "employee_id",
    "employee_name",
    "department"
]
employees = employees[employee_columns].drop_duplicates(
    subset="employee_id"
)

# Generate 30 days of sample attendance
start_date = datetime(2026, 9, 1)
attendance_records = []

for _, employee in employees.iterrows():
    for day in range(30):
        date = start_date + timedelta(days=day)

        # Monday-Friday only
        if date.weekday() >= 5:
            continue

        # Simulate occasional absences
        status = random.choices(
            ["Present", "Absent"],
            weights=[0.90, 0.10],
            k=1
        )[0]

        if status == "Present":
            clock_in_time = date.replace(
                hour=random.choice([8, 9]),
                minute=random.choice([0, 5, 10, 15, 30])
            )

            clock_out_time = date.replace(
                hour=random.choice([16, 17, 18]),
                minute=random.choice([0, 15, 30, 45])
            )

            # Ensure clock-out is after clock-in
            if clock_out_time <= clock_in_time:
                clock_out_time = clock_in_time + timedelta(hours=8)

        else:
            clock_in_time = None
            clock_out_time = None

        attendance_records.append({
            "employee_id": employee["employee_id"],
            "employee_name": employee["employee_name"],
            "department": employee["department"],
            "attendance_date": date.strftime("%Y-%m-%d"),
            "clock_in": (
                clock_in_time.strftime("%Y-%m-%d %H:%M:%S")
                if clock_in_time else None
            ),
            "clock_out": (
                clock_out_time.strftime("%Y-%m-%d %H:%M:%S")
                if clock_out_time else None
            ),
            "status": status
        })

attendance_df = pd.DataFrame(attendance_records)
attendance_df.to_csv("attendance_30days.csv", index=False)

# Generate sample task records
task_names = [
    "SQL reporting",
    "Data validation",
    "Monthly report",
    "Database testing",
    "Data cleaning",
    "Attendance analysis",
    "Dashboard update",
    "Documentation"
]

task_records = []
task_id = 1

for _, employee in employees.iterrows():
    # Generate 3-6 tasks per employee
    for _ in range(random.randint(3, 6)):
        task_date = start_date + timedelta(
            days=random.randint(0, 29)
        )

        status = random.choice(["Completed", "Pending"])

        tasks_completed = (
            random.randint(1, 5)
            if status == "Completed"
            else 0
        )

        task_records.append({
            "task_id": task_id,
            "employee_id": employee["employee_id"],
            "employee_name": employee["employee_name"],
            "department": employee["department"],
            "task_name": random.choice(task_names),
            "task_date": task_date.strftime("%Y-%m-%d"),
            "tasks_completed": tasks_completed,
            "task_status": status
        })

        task_id += 1

tasks_df = pd.DataFrame(task_records)
tasks_df.to_csv("tasks_sample.csv", index=False)

print("Sample data generated successfully!")
print("Employees:", len(employees))
print("Attendance records:", len(attendance_df))
print("Task records:", len(tasks_df))
print("\nAttendance status summary:")
print(attendance_df["status"].value_counts())
print("\nTask status summary:")
print(tasks_df["task_status"].value_counts())

print("\nFiles created:")
print("attendance_30days.csv")
print("tasks_sample.csv")