# Databricks notebook source
# MAGIC %sql
# MAGIC SHOW CATALOGS

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE databricks_deepikaa.default.bike_rides_raw (
# MAGIC     ride_id INT,
# MAGIC     station STRING,
# MAGIC     duration_min INT,
# MAGIC     fare DOUBLE,
# MAGIC     status STRING
# MAGIC )
# MAGIC USING DELTA;
# MAGIC  

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO databricks_deepikaa.default.bike_rides_raw VALUES
# MAGIC (1, 'Central', 20, 100.0, 'Completed'),
# MAGIC (2, 'Airport', 35, 180.0, 'Completed'),
# MAGIC (3, 'Metro', 15, 75.0, 'Cancelled'),
# MAGIC (4, 'Central', 40, 200.0, 'Completed'),
# MAGIC (5, 'University', 25, 125.0, 'Completed');

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM databricks_deepikaa.default.bike_rides_raw;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REFRESH STREAMING TABLE bike_bronze_sql
# MAGIC AS
# MAGIC SELECT *
# MAGIC FROM STREAM(databricks_deepikaa.default.bike_rides_raw);

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REFRESH STREAMING TABLE bike_bronze_sql
# MAGIC AS
# MAGIC SELECT *
# MAGIC FROM STREAM(databricks_deepikaa.default.bike_rides_raw);

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REFRESH STREAMING TABLE bike_silver_sql
# MAGIC AS
# MAGIC SELECT
# MAGIC     ride_id,
# MAGIC     station,
# MAGIC     duration_min,
# MAGIC     fare
# MAGIC FROM STREAM(bike_bronze_sql)
# MAGIC WHERE status = 'Completed'
# MAGIC   AND duration_min > 0
# MAGIC   AND fare > 0;

# COMMAND ----------

# DBTITLE 1,Revenue by station chart
import matplotlib.pyplot as plt

df = spark.sql("""
    SELECT station, COUNT(*) AS total_rides, SUM(fare) AS total_revenue
    FROM databricks_deepikaa.default.bike_silver_sql
    GROUP BY station
""")

pdf = df.toPandas()

plt.figure(figsize=(10, 5))
plt.bar(pdf["station"], pdf["total_revenue"])

plt.xlabel("Station")
plt.ylabel("Total Revenue (₹)")
plt.title("Bike Rental Revenue by Station")
plt.show()


# COMMAND ----------

plt.figure(figsize=(7, 7))

plt.pie(
    pdf["total_revenue"],
    labels=pdf["station"],
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Revenue Distribution by Station")
plt.show()

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REFRESH MATERIALIZED VIEW bike_gold_sql
# MAGIC AS
# MAGIC SELECT
# MAGIC     station,
# MAGIC     COUNT(*) AS total_rides,
# MAGIC     ROUND(SUM(fare), 2) AS total_revenue
# MAGIC FROM bike_silver_sql
# MAGIC GROUP BY station;

# COMMAND ----------

import matplotlib.pyplot as plt

df = spark.sql("""
    SELECT station, total_rides, total_revenue
    FROM databricks_deepikaa.default.bike_gold_sql
""")

pdf = df.toPandas()

# COMMAND ----------

plt.figure(figsize=(7, 7))
plt.pie(
    pdf["total_revenue"],
    labels=pdf["station"],
    autopct="%1.1f%%",
    startangle=90
)
plt.title("Revenue Distribution by Station")
plt.show()

# COMMAND ----------

pdf = pdf.sort_values("station")

plt.figure(figsize=(10, 5))

plt.plot(
    pdf["station"],
    pdf["total_revenue"],
    marker="o"
)

plt.xlabel("Station")
plt.ylabel("Total Revenue (₹)")
plt.title("Revenue by Station")
plt.grid(True)
plt.show()

# COMMAND ----------

plt.figure(figsize=(10, 5))

plt.scatter(
    pdf["total_rides"],
    pdf["total_revenue"],
    s=100
)

for _, row in pdf.iterrows():
    plt.annotate(
        row["station"],
        (row["total_rides"], row["total_revenue"]),
        xytext=(5, 5),
        textcoords="offset points"
    )

plt.xlabel("Total Rides")
plt.ylabel("Total Revenue (₹)")
plt.title("Total Rides vs Revenue")
plt.grid(True)
plt.show()