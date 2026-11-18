import pandas as pd

# Load cleaned task data
tasks = pd.read_csv("tasks_cleaned.csv")

print("===== TASK PRODUCTIVITY ANALYSIS =====")

# Check task records
print("\nTask records:")
print(tasks)

# Count task records by status
print("\nTask status summary:")
print(tasks["task_status"].value_counts())

# Calculate task totals for each employee
summary = tasks.groupby("employee_id").agg(
    employee_tasks=("task_id", "count"),
    tasks_completed=("tasks_completed", "sum")
).reset_index()

# Calculate completion rate only if task records
# represent individual tasks with a clear completion status.
print("\nTask summary by employee:")
print(summary)

# Save the report
summary.to_csv("employee_productivity_report.csv", index=False)

print("\nReport saved as employee_productivity_report.csv")
