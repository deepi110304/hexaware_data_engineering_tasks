
import pandas as pd

# Load cleaned attendance data
attendance = pd.read_csv("attendance_cleaned.csv")

# Convert date and time columns
attendance["attendance_date"] = pd.to_datetime(
    attendance["attendance_date"], errors="coerce"
)

attendance["clock_in"] = pd.to_datetime(
    attendance["clock_in"], errors="coerce"
)

attendance["clock_out"] = pd.to_datetime(
    attendance["clock_out"], errors="coerce"
)

# Calculate working hours
attendance["working_hours"] = (
    attendance["clock_out"] - attendance["clock_in"]
).dt.total_seconds() / 3600

# Only calculate hours for valid Present records
valid_records = (
    attendance["status"].eq("Present")
    & attendance["clock_in"].notna()
    & attendance["clock_out"].notna()
    & attendance["working_hours"].ge(0)
)

attendance.loc[~valid_records, "working_hours"] = pd.NA

# Display results
print("===== EMPLOYEE WORKING HOURS =====")

print(
    attendance[
        [
            "employee_id",
            "employee_name",
            "attendance_date",
            "clock_in",
            "clock_out",
            "status",
            "working_hours",
        ]
    ].to_string(index=False)
)

# Save the analysis
attendance.to_csv("working_hours_report.csv", index=False)

print("\nReport saved as working_hours_report.csv")
