import pandas as pd
from bson import json_util

print("===== EMPLOYEE AND FEEDBACK INTEGRATION =====")

# Step 1: Load employee data exported from MySQL
employees = pd.read_csv("employees_from_mysql.csv")

print("\nEmployee records loaded:", len(employees))

# Step 2: Load feedback data exported from MongoDB
with open("task_feedback_from_mongodb.json", "r", encoding="utf-8") as file:
    feedback_text = file.read()

feedback_records = json_util.loads(feedback_text)

# Convert feedback records into a Pandas DataFrame
feedback = pd.DataFrame(feedback_records)

print("Feedback records loaded:", len(feedback))

# Step 3: Convert MongoDB date values into readable strings
def convert_date(value):
    if value is None:
        return ""

    if hasattr(value, "isoformat"):
        return value.isoformat()

    return str(value)


feedback["created_at"] = feedback["created_at"].apply(convert_date)

# Step 4: Remove MongoDB's internal _id column
if "_id" in feedback.columns:
    feedback = feedback.drop(columns=["_id"])

# Step 5: Combine employee details and feedback
combined_data = pd.merge(
    employees,
    feedback,
    on="employee_id",
    how="left"
)

# Step 6: Save the combined report
output_file = "employee_feedback_report.csv"
combined_data.to_csv(output_file, index=False)

# Step 7: Display the report
print("\n===== COMBINED EMPLOYEE FEEDBACK REPORT =====")
print(combined_data.to_string(index=False))

print("\n===== SUMMARY =====")
print("Total employees:", len(employees))
print("Total feedback records:", len(feedback))
print("Total rows in combined report:", len(combined_data))
print("Report saved as:", output_file)

print("\nIntegration completed successfully!")