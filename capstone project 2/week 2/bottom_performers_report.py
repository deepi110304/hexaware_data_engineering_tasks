import pandas as pd

print("===== BOTTOM PERFORMERS REPORT =====")

# Step 1: Load the Week 2 summary report
df = pd.read_csv("final_week2_report.csv")

print("\nColumns available:")
print(df.columns.tolist())

# Step 2: Check required columns
required_columns = [
    "employee_name",
    "department",
    "productivity_score"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    print("\nMissing required columns:", missing_columns)
    print("Please check the column names in final_week2_report.csv.")
else:
    # Step 3: Convert productivity scores to numeric values
    df["productivity_score"] = pd.to_numeric(
        df["productivity_score"],
        errors="coerce"
    )

    # Exclude records where productivity cannot be calculated
    valid_data = df.dropna(subset=["productivity_score"]).copy()

    # Step 4: Sort from lowest to highest productivity
    bottom_performers = valid_data.sort_values(
        by="productivity_score",
        ascending=True
    ).head(5)

    # Step 5: Save the bottom 5 report
    bottom_performers.to_csv(
        "bottom_performers_report.csv",
        index=False
    )

    # Step 6: Display the report
    print("\n===== BOTTOM 5 PERFORMERS =====")

    print(
        bottom_performers[
            ["employee_name", "department", "productivity_score"]
        ].to_string(index=False)
    )

    print("\nReport saved as bottom_performers_report.csv")
    print("\nBottom-performer report generated successfully!")
    print(
        "\nNote: These results use the project's simulated "
        "attendance and task data."
    )