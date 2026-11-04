# Databricks notebook source
path = "/Workspace/Users/azuser7401_mml.local@karthikirisoutlook.onmicrosoft.com/cinema_bookings.csv"
df = spark.read.csv(
    "file:" + path,
    header=True,
    inferSchema=True
)
display(df)

# COMMAND ----------

path = "/Workspace/Users/azuser7401_mml.local@karthikirisoutlook.onmicrosoft.com/cinema_master.json"
df = spark.read.csv(
    "file:" + path,
    header=True,
    inferSchema=True
)
display(df)

# COMMAND ----------

# DBTITLE 1,Load bookings and print schema
csv_path = "file:/Workspace/Users/azuser7401_mml.local@karthikirisoutlook.onmicrosoft.com/cinema_bookings.csv"
bookings_df = spark.read.csv(csv_path, header=True, inferSchema=True)
bookings_df.printSchema()

# COMMAND ----------

csv_path = "file:/Workspace/Users/azuser7401_mml.local@karthikirisoutlook.onmicrosoft.com/cinema_master.json"
cinema_df = spark.read.csv(csv_path, header=True, inferSchema=True)
cinema_df.printSchema()

# COMMAND ----------

bookings_df.show(10, truncate=False)
print(f"Total CSV Rows: {bookings_df.count()}")

# COMMAND ----------

selected_df = bookings_df.select(
    "booking_id",
    "movie_title",
    "tickets",
    "booking_status"
)
display(selected_df)

# COMMAND ----------

from pyspark.sql.functions import col
confirmed_df = bookings_df.filter(
    col("booking_status") == "Confirmed"
)
display(confirmed_df)

# COMMAND ----------

filtered_df = bookings_df.filter(
    (col("tickets") > 3) &
    (col("price_per_ticket") > 200)
)
display(filtered_df)

# COMMAND ----------

# DBTITLE 1,Count missing values
from pyspark.sql import functions as F
missing_df = bookings_df.select(
    F.sum(col("discount_pct").isNull().cast("int")).alias("missing_discount"),
    F.sum(col("payment_method").isNull().cast("int")).alias("missing_payment")
)
display(missing_df)

# COMMAND ----------

cleaned_df = bookings_df.fillna({
    "discount_pct": 0,
    "payment_method": "Unknown"
})
display(cleaned_df)

# COMMAND ----------

cleaned_df = cleaned_df.withColumn(
    "gross_amount",
    col("tickets") * col("price_per_ticket")
)
display(cleaned_df)

# COMMAND ----------

cleaned_df = cleaned_df.withColumn(
    "net_amount",
    col("gross_amount") *
    (1 - col("discount_pct") / 100)
)
display(cleaned_df)

# COMMAND ----------

# DBTITLE 1,Add booking size category
from pyspark.sql.functions import when
cleaned_df = cleaned_df.withColumn(
    "booking_size",
    when(col("tickets") >= 4, "Large")
    .otherwise("Regular")
)
display(cleaned_df)

# COMMAND ----------

top_bookings_df = cleaned_df.orderBy(
    col("net_amount").desc()
)
display(top_bookings_df.limit(5))

# COMMAND ----------

from pyspark.sql.functions import count
status_count_df = bookings_df.groupBy(
    "booking_status"
).agg(
    count("*").alias("total_bookings")
)
display(status_count_df)

# COMMAND ----------

from pyspark.sql.functions import col, sum
movie_revenue_df = cleaned_df.filter(
    col("booking_status") == "Confirmed"
).groupBy(
    "movie_title"
).agg(
    sum("tickets").alias("total_tickets"),
    sum("net_amount").alias("net_revenue")
)
display(movie_revenue_df)

# COMMAND ----------

cinema_revenue_df = cleaned_df.filter(
    col("booking_status") == "Confirmed"
).groupBy(
    "cinema_id"
).agg(
    sum("net_amount").alias("total_net_revenue")
).orderBy(
    col("total_net_revenue").desc()
)
display(cinema_revenue_df.limit(3))

# COMMAND ----------

cinema_master_df = spark.read.json("file:/Workspace/Users/azuser7401_mml.local@karthikirisoutlook.onmicrosoft.com/cinema_master.json")
joined_df = cleaned_df.join(cinema_master_df, on="cinema_id", how="inner")
cinema_details_df = joined_df.select(
    "cinema_name",
    col("location.city").alias("city"),
    "movie_title",
    "booking_status"
)
display(cinema_details_df)

# COMMAND ----------

unmatched_df = joined_df.filter(
    col("cinema_name").isNull()
)
display(unmatched_df)

# COMMAND ----------

zone_df = cinema_master_df.select(
    "cinema_name",
    col("location.zone").alias("zone")
)
display(zone_df)

# COMMAND ----------

# DBTITLE 1,Explode cinema facilities
from pyspark.sql.functions import explode
facilities_df = cinema_master_df.select(
    "cinema_name",
    explode("facilities").alias("facility")
)
display(facilities_df)

# COMMAND ----------

# DBTITLE 1,Days between booking and show
from pyspark.sql.functions import to_date, datediff
date_df = cleaned_df.withColumn(
    "booking_date",
    to_date(col("booking_date"), "yyyy-MM-dd")
).withColumn(
    "show_date",
    to_date(col("show_date"), "yyyy-MM-dd")
).withColumn(
    "days_between_booking_and_show",
    datediff(col("show_date"), col("booking_date"))
)
display(date_df)

# COMMAND ----------

duplicate_df = bookings_df.groupBy(
    "booking_id"
).agg(
    count("*").alias("record_count")
).filter(
    col("record_count") > 1
)
display(duplicate_df)

# COMMAND ----------

deduplicated_df = date_df.dropDuplicates(
    ["booking_id"]
)
display(deduplicated_df)

# COMMAND ----------

print("Original Rows:", bookings_df.count())
print("Rows After Deduplication:", deduplicated_df.count())

# COMMAND ----------

from pyspark.sql.functions import sum, col, dense_rank
from pyspark.sql.window import Window
movie_rank_df = cleaned_df.filter(
    col("booking_status") == "Confirmed"
).groupBy(
    "movie_title"
).agg(
    sum("net_amount").alias("total_net_revenue")
)
window_spec = Window.orderBy(
    col("total_net_revenue").desc()
)
ranked_movies_df = movie_rank_df.withColumn(
    "movie_rank",
    dense_rank().over(window_spec)
)
display(ranked_movies_df)

# COMMAND ----------

# DBTITLE 1,Final bookings with cinema details
final_df = deduplicated_df.join(
    cinema_master_df,
    on="cinema_id",
    how="left"
)
display(final_df)

# COMMAND ----------

final_df.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("cinema_booking_cleaned")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM cinema_booking_cleaned LIMIT 5;

# COMMAND ----------

report_df = bookings_df.fillna({
    "discount_pct": 0,
    "payment_method": "Unknown"
})

# COMMAND ----------

report_df = report_df.dropDuplicates(
    ["booking_id"]
)

# COMMAND ----------

report_df = report_df.withColumn(
    "gross_amount",
    col("tickets") * col("price_per_ticket")
)

# COMMAND ----------

report_df = report_df.withColumn(
    "net_amount",
    col("gross_amount") *
    (1 - col("discount_pct") / 100)
)

# COMMAND ----------

# DBTITLE 1,Join report with cinema details
report_df = report_df.join(
    cinema_master_df,
    on="cinema_id",
    how="left"
)

# COMMAND ----------

report_df = report_df.filter(
    col("booking_status") == "Confirmed"
)

# COMMAND ----------

# Step 7: Group by city and movie
performance_df = report_df.groupBy(
    col("location.city").alias("city"),
    "movie_title"
).agg(
    sum("tickets").alias("total_tickets"),
    sum("net_amount").alias("total_net_revenue")
)

# COMMAND ----------

display(performance_df)

# COMMAND ----------

performance_df.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("cinema_performance_report")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM cinema_performance_report
# MAGIC ORDER BY total_net_revenue DESC;