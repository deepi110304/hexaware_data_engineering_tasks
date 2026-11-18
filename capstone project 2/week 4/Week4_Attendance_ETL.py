# Databricks notebook source
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
spark = SparkSession.builder \
    .appName("Employee_Attendance_ETL") \
    .getOrCreate()
print("Spark session created successfully!")
print("Spark Version:", spark.version)

# COMMAND ----------

from pyspark.sql import functions as F
# Define input file paths
attendance_path = "/Workspace/Users/deepikaa1103@gmail.com/attendance_30days_with_breaks.csv"
tasks_path = "/Workspace/Users/deepikaa1103@gmail.com/tasks_sample.csv"
employees_path = "/Workspace/Users/deepikaa1103@gmail.com/employees_from_mysql.csv"
# Load attendance dataset
attendance_df = spark.read.csv(
    attendance_path,
    header=True,
    inferSchema=True
)
# Load task dataset
tasks_df = spark.read.csv(
    tasks_path,
    header=True,
    inferSchema=True
)
# Load employee dataset
employees_df = spark.read.csv(
    employees_path,
    header=True,
    inferSchema=True
)
print("All three datasets loaded successfully!")

# COMMAND ----------

print("===== ATTENDANCE DATA =====")
attendance_df.show(5, truncate=False)
attendance_df.printSchema()
print("===== TASK DATA =====")
tasks_df.show(5, truncate=False)
tasks_df.printSchema()
print("===== EMPLOYEE DATA =====")
employees_df.show(5, truncate=False)
employees_df.printSchema()
print("===== RECORD COUNTS =====")
print("Attendance records:", attendance_df.count())
print("Task records:", tasks_df.count())
print("Employee records:", employees_df.count())

# COMMAND ----------

# Remove duplicate records
attendance_cleaned = attendance_df.dropDuplicates()
# Remove records with missing employee IDs or attendance status
attendance_cleaned = attendance_cleaned.dropna(
    subset=["employee_id", "status"]
)
# Standardise attendance status
attendance_cleaned = attendance_cleaned.withColumn(
    "status",
    F.initcap(F.trim(F.col("status")))
)
print("Attendance cleaning completed!")
attendance_cleaned.show(5)

# COMMAND ----------

tasks_cleaned = tasks_df.dropDuplicates()
tasks_cleaned = tasks_cleaned.dropna(
    subset=["employee_id", "task_status"]
)
tasks_cleaned = tasks_cleaned.withColumn(
    "task_status",
    F.initcap(F.trim(F.col("task_status")))
)
print("Task data cleaning completed!")
tasks_cleaned.show(5)

# COMMAND ----------

attendance_combined = attendance_cleaned.join(
    employees_df.select(
        "employee_id",
        "employee_name",
        "department"
    ),
    on="employee_id",
    how="left"
)
print("Attendance and employee data combined!")
attendance_combined.show(10)

# COMMAND ----------

# Disambiguate duplicate employee_name/department columns created by the join
cols = attendance_combined.columns
attendance_dedup = attendance_combined.toDF(*[
    c if cols[:i].count(c) == 0 else f"{c}_dup" for i, c in enumerate(cols)
]).drop("employee_name_dup", "department_dup")
attendance_kpis = attendance_dedup.groupBy(
    "employee_id",
    "employee_name",
    "department"
).agg(
    F.count("*").alias("total_attendance_days"),
    F.sum(
        F.when(F.col("status") == "Present", 1).otherwise(0)
    ).alias("present_days"),

    F.sum(
        F.when(F.col("status") == "Absent", 1).otherwise(0)
    ).alias("absent_days")
)
attendance_kpis = attendance_kpis.withColumn(
    "attendance_percentage",
    F.round(
        F.col("present_days") /
        F.col("total_attendance_days") * 100,
        2
    )
)
attendance_kpis.show()

# COMMAND ----------

tasks_combined = tasks_cleaned.join(
    employees_df.select(
        "employee_id",
        "department"
    ),
    on="employee_id",
    how="left"
)

# Disambiguate duplicate department column created by the join
cols = tasks_combined.columns
tasks_combined = tasks_combined.toDF(*[
    c if cols[:i].count(c) == 0 else f"{c}_dup" for i, c in enumerate(cols)
]).drop("department_dup")

task_kpis = tasks_combined.groupBy(
    "department"
).agg(
    F.count("*").alias("total_task_records"),

    F.sum(
        F.when(F.col("task_status") == "Completed", 1).otherwise(0)
    ).alias("completed_task_records"),

    F.sum("tasks_completed").alias("total_tasks_completed")
)

task_kpis.show()

# COMMAND ----------

# Build combined department KPIs: roll up attendance KPIs to department level and join task KPIs
department_attendance = attendance_kpis.groupBy(
    "department"
).agg(
    F.sum("total_attendance_days").alias("total_attendance_days"),
    F.sum("present_days").alias("present_days"),
    F.sum("absent_days").alias("absent_days")
)
department_attendance = department_attendance.withColumn(
    "attendance_percentage",
    F.round(
        F.col("present_days") /
        F.col("total_attendance_days") * 100,
        2
    )
)
department_kpis = department_attendance.join(
    task_kpis,
    on="department",
    how="outer"
)
department_kpis.show()

# Save as Delta format
department_kpis.write \
    .format("delta") \
    .mode("overwrite") \
    .save("/Volumes/workspace/default/week4_outputs/week4_department_kpis_delta")

# Save as CSV format
department_kpis.coalesce(1).write \
    .option("header", True) \
    .mode("overwrite") \
    .csv("/Volumes/workspace/default/week4_outputs/week4_department_kpis_csv")

print("Week 4 ETL process completed!")
print("Delta and CSV outputs saved successfully!")