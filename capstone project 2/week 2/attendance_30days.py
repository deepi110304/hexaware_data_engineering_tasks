import pandas as pd

# Load the 30-day attendance dataset
df = pd.read_csv("attendance_30days.csv")

# Convert date and time columns
df["attendance_date"] = pd.to_datetime(df["attendance_date"], errors="coerce")
df["clock_in"] = pd.to_datetime(df["clock_in"], errors="coerce")
df["clock_out"] = pd.to_datetime(df["clock_out"], errors="coerce")

# Calculate working hours
df["working_hours"] = (
    df["clock_out"] - df["clock_in"]
).dt.total_seconds() / 3600

# Do not count absent days as working hours
df.loc[df["status"] == "Absent", "working_hours"] = pd.NA

# Display attendance statistics
print("===== 30-DAY ATTENDANCE ANALYSIS =====")
print("\nAttendance status counts:")
print(df["status"].value_counts())

# Summarize each employee
summary = df.groupby(
    ["employee_id", "employee_name", "department"]
).agg(
    attendance_days=("status", "size"),
    present_days=("status", lambda x: (x == "Present").sum()),
    absent_days=("status", lambda x: (x == "Absent").sum()),
    total_working_hours=("working_hours", "sum")
).reset_index()

summary["attendance_rate_percent"] = (
    summary["present_days"] / summary["attendance_days"] * 100
).round(2)

summary["total_working_hours"] = summary["total_working_hours"].round(2)

print("\n===== EMPLOYEE SUMMARY =====")
print(summary.to_string(index=False))

# Save the report
summary.to_csv("attendance_30day_summary.csv", index=False)

print("\nReport saved: attendance_30day_summary.csv")