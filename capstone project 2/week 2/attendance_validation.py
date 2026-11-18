import pandas as pd

# Load the working-hours report
df = pd.read_csv("working_hours_report.csv")

print("===== ATTENDANCE VALIDATION =====")

# 1. Check for missing attendance dates
missing_dates = df[df["attendance_date"].isna()]

print("\nEmployees without attendance dates:")
print(missing_dates[["employee_id", "employee_name"]])

# 2. Check for missing clock-in or clock-out times
incomplete_times = df[
    df["attendance_date"].notna()
    & (
        df["clock_in"].isna()
        | df["clock_out"].isna()
    )
]

print("\nRecords with incomplete clock times:")
print(incomplete_times[["employee_name", "status"]])

# 3. Check for negative working hours
invalid_hours = df[df["working_hours"] < 0]

print("\nRecords with negative working hours:")
print(invalid_hours[["employee_name", "working_hours"]])

# 4. Flag unusually short shifts under one hour
short_shifts = df[
    df["working_hours"].notna()
    & (df["working_hours"] < 1)
]

print("\nShifts shorter than one hour:")
print(short_shifts[["employee_name", "attendance_date", "working_hours"]])

# 5. Save validation results
df["validation_issue"] = ""

df.loc[
    df["attendance_date"].isna(),
    "validation_issue"
] = "No attendance record"

df.loc[
    df["attendance_date"].notna()
    & df["clock_in"].isna(),
    "validation_issue"
] = "Missing clock-in"

df.loc[
    df["attendance_date"].notna()
    & df["clock_out"].isna(),
    "validation_issue"
] = "Missing clock-out"

df.loc[
    df["working_hours"] < 0,
    "validation_issue"
] = "Negative working hours"

df.to_csv("attendance_validation_report.csv", index=False)

print("\nValidation report saved successfully!")