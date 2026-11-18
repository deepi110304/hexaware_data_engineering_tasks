import pandas as pd
import numpy as np

# ==========================================
# STEP 1: LOAD DATASETS
# ==========================================

attendance = pd.read_csv("attendance_30days_with_breaks.csv")
tasks = pd.read_csv("tasks_sample.csv")

print("Attendance dataset loaded:", attendance.shape)
print("Task dataset loaded:", tasks.shape)


# ==========================================
# STEP 2: CLEAN AND VALIDATE DATA
# ==========================================

# Convert dates and times into appropriate formats
attendance["attendance_date"] = pd.to_datetime(
    attendance["attendance_date"], errors="coerce"
)

attendance["clock_in"] = pd.to_datetime(
    attendance["clock_in"], errors="coerce"
)

attendance["clock_out"] = pd.to_datetime(
    attendance["clock_out"], errors="coerce"
)

# Convert numeric columns safely
attendance["break_minutes"] = pd.to_numeric(
    attendance["break_minutes"], errors="coerce"
)

# Check required columns
required_attendance_columns = [
    "employee_id",
    "employee_name",
    "department",
    "attendance_date",
    "clock_in",
    "clock_out",
    "status",
    "break_minutes"
]

missing_columns = [
    column for column in required_attendance_columns
    if column not in attendance.columns
]

if missing_columns:
    raise ValueError(
        f"Missing attendance columns: {missing_columns}"
    )

required_task_columns = [
    "employee_id",
    "task_id",
    "task_status",
    "tasks_completed"
]

missing_task_columns = [
    column for column in required_task_columns
    if column not in tasks.columns
]

if missing_task_columns:
    raise ValueError(
        f"Missing task columns: {missing_task_columns}"
    )

# Remove duplicate attendance records using employee ID and date
attendance_duplicates = attendance.duplicated(
    subset=["employee_id", "attendance_date"]
)

print(
    "\nDuplicate attendance records found:",
    attendance_duplicates.sum()
)

attendance = attendance.drop_duplicates(
    subset=["employee_id", "attendance_date"],
    keep="first"
).copy()

# Normalize attendance status
attendance["status"] = (
    attendance["status"].astype("string").str.strip().str.title()
)

# Keep only recognized attendance statuses
valid_statuses = ["Present", "Absent"]

invalid_status_count = (~attendance["status"].isin(valid_statuses)).sum()

print("Invalid attendance statuses:", invalid_status_count)

attendance = attendance[
    attendance["status"].isin(valid_statuses)
].copy()

# Convert task values into numeric format
tasks["tasks_completed"] = pd.to_numeric(
    tasks["tasks_completed"], errors="coerce"
)

# Normalize task status
tasks["task_status"] = (
    tasks["task_status"].astype("string").str.strip().str.title()
)

# Remove duplicate task records when task IDs are available
task_duplicates = tasks.duplicated(subset=["task_id"])

print("Duplicate task records found:", task_duplicates.sum())

tasks = tasks.drop_duplicates(
    subset=["task_id"],
    keep="first"
).copy()

# Treat missing task counts as zero for this report
tasks["tasks_completed"] = tasks["tasks_completed"].fillna(0)

# Ensure task counts are non-negative
tasks.loc[
    tasks["tasks_completed"] < 0,
    "tasks_completed"
] = 0


# ==========================================
# STEP 3: CALCULATE SHIFT HOURS
# ==========================================

attendance["total_shift_hours"] = (
    attendance["clock_out"] - attendance["clock_in"]
).dt.total_seconds() / 3600

# A valid shift requires Present status and valid clock times
valid_shift = (
    (attendance["status"] == "Present")
    & attendance["clock_in"].notna()
    & attendance["clock_out"].notna()
    & (attendance["total_shift_hours"] >= 0)
)

# Invalid and absent shifts do not contribute working hours
attendance.loc[
    ~valid_shift,
    "total_shift_hours"
] = np.nan


# ==========================================
# STEP 4: CALCULATE BREAK HOURS
# ==========================================

# Break values are simulated sample data.
# Do not treat them as actual employee break records.

# Validate break duration
invalid_break = (
    attendance["break_minutes"].isna()
    | (attendance["break_minutes"] < 0)
)

print(
    "Invalid break-duration records:",
    invalid_break.sum()
)

# Only Present records with valid shifts receive break-hour values
attendance["break_hours"] = np.where(
    valid_shift & ~invalid_break,
    attendance["break_minutes"] / 60,
    np.nan
)


# ==========================================
# STEP 5: CALCULATE NET WORKING HOURS
# ==========================================

attendance["net_working_hours"] = (
    attendance["total_shift_hours"]
    - attendance["break_hours"]
)

# Negative net working hours are invalid
invalid_net_hours = (
    attendance["net_working_hours"] < 0
)

attendance.loc[
    invalid_net_hours,
    "net_working_hours"
] = np.nan

print(
    "\nAttendance records after validation:",
    attendance.shape
)


# ==========================================
# STEP 6: EXPORT CLEANED DATASETS
# ==========================================

attendance.to_csv(
    "attendance_30days_cleaned.csv",
    index=False
)

tasks.to_csv(
    "tasks_sample_cleaned.csv",
    index=False
)

print("\nCleaned attendance saved as attendance_30days_cleaned.csv")
print("Cleaned tasks saved as tasks_sample_cleaned.csv")


# ==========================================
# STEP 7: SUMMARIZE ATTENDANCE
# ==========================================

attendance_summary = attendance.groupby(
    ["employee_id", "employee_name", "department"],
    dropna=False
).agg(
    attendance_days=("status", "size"),

    present_days=(
        "status",
        lambda values: (values == "Present").sum()
    ),

    absent_days=(
        "status",
        lambda values: (values == "Absent").sum()
    ),

    total_shift_hours=(
        "total_shift_hours",
        "sum"
    ),

    total_break_hours=(
        "break_hours",
        "sum"
    ),

    total_net_working_hours=(
        "net_working_hours",
        "sum"
    )
).reset_index()


# ==========================================
# STEP 8: CALCULATE ATTENDANCE RATE
# ==========================================

attendance_summary["attendance_rate_percent"] = np.where(
    attendance_summary["attendance_days"] > 0,

    attendance_summary["present_days"]
    / attendance_summary["attendance_days"] * 100,

    0
).round(2)


# ==========================================
# STEP 9: SUMMARIZE TASK PERFORMANCE
# ==========================================

# Use the task records to calculate completed task records
task_summary = tasks.groupby("employee_id").agg(
    total_task_records=("task_id", "count"),

    completed_task_records=(
        "task_status",
        lambda values: (values == "Completed").sum()
    ),

    total_tasks_completed=(
        "tasks_completed",
        "sum"
    )
).reset_index()


# ==========================================
# STEP 10: CALCULATE TASK COMPLETION RATE
# ==========================================

task_summary["task_completion_rate_percent"] = np.where(
    task_summary["total_task_records"] > 0,

    task_summary["completed_task_records"]
    / task_summary["total_task_records"] * 100,

    0
).round(2)


# ==========================================
# STEP 11: MERGE ATTENDANCE AND TASK DATA
# ==========================================

report = attendance_summary.merge(
    task_summary,
    on="employee_id",
    how="left"
)

# Employees without task records have missing task information.
# Zero here means zero recorded tasks in the available dataset,
# not necessarily zero real-world work performed.

report["total_task_records"] = (
    report["total_task_records"].fillna(0).astype(int)
)

report["completed_task_records"] = (
    report["completed_task_records"].fillna(0).astype(int)
)

report["total_tasks_completed"] = (
    report["total_tasks_completed"].fillna(0)
)

report["task_completion_rate_percent"] = (
    report["task_completion_rate_percent"].fillna(0)
)


# ==========================================
# STEP 12: CALCULATE PRODUCTIVITY SCORE
# ==========================================

# Productivity score = completed task units / net working hours

report["productivity_score"] = np.where(
    report["total_net_working_hours"] > 0,

    report["total_tasks_completed"]
    / report["total_net_working_hours"],

    np.nan
).round(3)


# ==========================================
# STEP 13: DISPLAY FINAL EMPLOYEE REPORT
# ==========================================

print("\n==========================================")
print("          FINAL WEEK 2 REPORT")
print("==========================================")

columns_to_display = [
    "employee_name",
    "department",
    "present_days",
    "absent_days",
    "attendance_rate_percent",
    "total_shift_hours",
    "total_break_hours",
    "total_net_working_hours",
    "total_tasks_completed",
    "task_completion_rate_percent",
    "productivity_score"
]

print(
    report[columns_to_display].round(2).to_string(index=False)
)


# ==========================================
# STEP 14: IDENTIFY FREQUENT ABSENTEES
# ==========================================

print("\n==========================================")
print("           FREQUENT ABSENTEES")
print("==========================================")

frequent_absentees = report[
    ["employee_name", "department", "absent_days"]
].sort_values(
    by=["absent_days", "employee_name"],
    ascending=[False, True]
)

print(frequent_absentees.to_string(index=False))


# ==========================================
# STEP 15: IDENTIFY TOP PERFORMERS
# ==========================================

print("\n==========================================")
print(" TOP 5 BY PRODUCTIVITY SCORE")
print("==========================================")

top_performers = report[
    [
        "employee_name",
        "department",
        "productivity_score"
    ]
].dropna().sort_values(
    by="productivity_score",
    ascending=False
).head(5)

print(top_performers.to_string(index=False))


# ==========================================
# STEP 16: SAVE FINAL REPORT
# ==========================================

report.to_csv(
    "final_week2_report.csv",
    index=False
)

frequent_absentees.to_csv(
    "frequent_absentees_report.csv",
    index=False
)

top_performers.to_csv(
    "top_performers_report.csv",
    index=False
)

print("\n==========================================")
print("             FILES CREATED")
print("==========================================")

print("1. attendance_30days_cleaned.csv")
print("2. tasks_sample_cleaned.csv")
print("3. final_week2_report.csv")
print("4. frequent_absentees_report.csv")
print("5. top_performers_report.csv")

print("\nWeek 2 report generation completed successfully!")

print(
    "\nNote: Attendance and task data are simulated. "
    "Break durations are also simulated."
)