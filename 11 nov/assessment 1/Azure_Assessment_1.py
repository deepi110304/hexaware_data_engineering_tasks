# Databricks notebook source
CATALOG = "workspace"
SCHEMA = "default"

BASE_PATH = "/Volumes/workspace/default/themepark_files"

prefix = f"{CATALOG}.{SCHEMA}"

print(BASE_PATH)

# COMMAND ----------

display(dbutils.fs.ls(BASE_PATH))

# COMMAND ----------

CATALOG = "workspace"
SCHEMA = "default"

tables = [
    "tp_entries_raw",
    "tp_attractions",
    "tp_maintenance",
    "tp_entry_changes"
]

for table in tables:
    full_name = f"{CATALOG}.{SCHEMA}.{table}"

    df = spark.table(full_name)

    print(f"\nTable: {table}")
    print(f"Total rows: {df.count()}")
    df.printSchema()

# COMMAND ----------

display(
    spark.table("workspace.default.tp_entries_raw")
)

# COMMAND ----------

SECTION A

# COMMAND ----------

entries_df = spark.table("workspace.default.tp_entries_raw")
attractions_df = spark.table("workspace.default.tp_attractions")
maintenance_df = spark.table("workspace.default.tp_maintenance")
changes_df = spark.table("workspace.default.tp_entry_changes")
print("Visitor Entries:", entries_df.count())
print("Attractions:", attractions_df.count())
print("Maintenance Records:", maintenance_df.count())
print("Entry Changes:", changes_df.count())
display(entries_df)
display(attractions_df)
display(maintenance_df)
display(changes_df)

# COMMAND ----------

entries_df.printSchema()

# COMMAND ----------

selected_df = entries_df.select(
    "entry_id",
    "attraction_id",
    "visit_date",
    "ticket_type",
    "ticket_price"
)
display(selected_df.limit(20))

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM workspace.default.tp_entries_raw
# MAGIC WHERE status = 'Completed'
# MAGIC AND ticket_price > 500;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT DISTINCT ticket_type
# MAGIC FROM workspace.default.tp_entries_raw;
# MAGIC SELECT DISTINCT booking_channel
# MAGIC FROM workspace.default.tp_entries_raw;
# MAGIC SELECT *
# MAGIC FROM workspace.default.tp_entries_raw
# MAGIC WHERE ticket_type IN ('Standard', 'Express');
# MAGIC SELECT *
# MAGIC FROM workspace.default.tp_entries_raw
# MAGIC WHERE booking_channel IN ('App', 'Web');

# COMMAND ----------

# DBTITLE 1,Cell 10

from pyspark.sql import functions as F
dated_df = entries_df.withColumn(
    "visit_date",
    F.to_date("visit_date")
)
date_count_df = dated_df.groupBy(
    "visit_date"
).agg(
    F.count("*").alias("total_entries")
).orderBy("visit_date")
display(date_count_df)

# COMMAND ----------

SECTION B

# COMMAND ----------

missing_df = entries_df.filter(
    F.col("ticket_price").isNull() |
    F.col("booking_channel").isNull()
)
display(missing_df)
print("Missing records:", missing_df.count())

# COMMAND ----------

filled_df = entries_df.fillna({
    "booking_channel": "Unknown"
})
display(filled_df)

# COMMAND ----------

invalid_df = entries_df.filter(
    (F.col("wait_minutes") < 0) |
    (F.col("ride_minutes") == 0) |
    (F.col("ticket_price") <= 0)
)
display(invalid_df)
print("Invalid records:", invalid_df.count())

# COMMAND ----------

duplicate_ids_df = entries_df.groupBy(
    "entry_id"
).count().filter(
    F.col("count") > 1
)
print("Duplicate entry IDs:")
display(duplicate_ids_df)
deduplicated_df = entries_df.dropDuplicates(
    ["entry_id"]
)
print("Original count:", entries_df.count())
print("Deduplicated count:", deduplicated_df.count())
display(deduplicated_df)

# COMMAND ----------

unknown_attractions_df = entries_df.join(
    attractions_df.select("attraction_id"),
    on="attraction_id",
    how="left_anti"
)
display(unknown_attractions_df)

# COMMAND ----------

valid_wait_df = entries_df.filter(
    F.col("wait_minutes").isNotNull() &
    (F.col("wait_minutes") >= 0)
)
wait_category_df = valid_wait_df.withColumn(
    "wait_category",
    F.when(F.col("wait_minutes") <= 20, "Short")
    .when(F.col("wait_minutes") <= 45, "Medium")
    .otherwise("Long")
)
display(wait_category_df)

# COMMAND ----------

joined_df = entries_df.join(
    attractions_df,
    on="attraction_id",
    how="inner"
)
attraction_details_df = joined_df.select(
    "entry_id",
    "attraction_id",
    "attraction_name",
    "category",
    F.col("location.zone").alias("zone"),
    F.col("features").alias("features"),
    "ticket_price",
    "wait_minutes"
)
display(attraction_details_df)

# COMMAND ----------

SECTION C

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM workspace.default.tp_entries_raw
# MAGIC WHERE status = 'Completed'
# MAGIC AND ticket_type IN ('Standard', 'Express')
# MAGIC AND TO_DATE(visit_date)
# MAGIC     BETWEEN DATE '2026-01-01' AND DATE '2026-12-31';

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     attraction_id,
# MAGIC     SUM(ticket_price) AS total_revenue,
# MAGIC     COUNT(*) AS completed_entries
# MAGIC FROM workspace.default.tp_entries_raw
# MAGIC WHERE status = 'Completed'
# MAGIC AND ticket_price > 0
# MAGIC GROUP BY attraction_id
# MAGIC ORDER BY total_revenue DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     a.category,
# MAGIC     ROUND(AVG(e.wait_minutes), 2) AS average_wait_minutes
# MAGIC FROM workspace.default.tp_entries_raw e
# MAGIC INNER JOIN workspace.default.tp_attractions a
# MAGIC ON e.attraction_id = a.attraction_id
# MAGIC WHERE e.wait_minutes >= 0
# MAGIC GROUP BY a.category
# MAGIC ORDER BY average_wait_minutes DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     a.attraction_id,
# MAGIC     a.attraction_name,
# MAGIC     SUM(m.downtime_minutes) AS total_downtime
# MAGIC FROM workspace.default.tp_maintenance m
# MAGIC INNER JOIN workspace.default.tp_attractions a
# MAGIC ON m.attraction_id = a.attraction_id
# MAGIC WHERE m.maintenance_status = 'Completed'
# MAGIC GROUP BY
# MAGIC     a.attraction_id,
# MAGIC     a.attraction_name
# MAGIC ORDER BY total_downtime DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     a.location.zone AS park_zone,
# MAGIC     SUM(e.ticket_price) AS total_revenue
# MAGIC FROM workspace.default.tp_entries_raw e
# MAGIC INNER JOIN workspace.default.tp_attractions a
# MAGIC ON e.attraction_id = a.attraction_id
# MAGIC WHERE e.status = 'Completed'
# MAGIC AND e.ticket_price > 0
# MAGIC GROUP BY a.location.zone
# MAGIC ORDER BY total_revenue DESC;

# COMMAND ----------

                     SECTION D

# COMMAND ----------

# DBTITLE 1,Cell 27
clean_entries_df = (
    entries_df
    .filter(
        (F.col("ticket_price") > 0) &
        (F.col("wait_minutes") >= 0) &
        (F.col("ride_minutes") > 0) &
        F.col("attraction_id").isNotNull()
    )
    .fillna({"booking_channel": "Unknown"})
    .dropDuplicates(["entry_id"])
)
clean_entries_df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("workspace.default.tp_entries_work")
display(spark.table("workspace.default.tp_entries_work"))

# COMMAND ----------

# DBTITLE 1,Cell 28
clean_entries_df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("workspace.default.tp_entries_backup")
print("Backup Delta table created")
display(spark.table("workspace.default.tp_entries_backup"))

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE workspace.default.tp_entries_work;

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO workspace.default.tp_entries_work
# MAGIC (
# MAGIC     entry_id,
# MAGIC     visitor_id,
# MAGIC     attraction_id,
# MAGIC     visit_date,
# MAGIC     entry_time,
# MAGIC     wait_minutes,
# MAGIC     ride_minutes,
# MAGIC     ticket_type,
# MAGIC     ticket_price,
# MAGIC     status,
# MAGIC     booking_channel
# MAGIC )
# MAGIC VALUES
# MAGIC (9001, 'V901', 'A01', '2026-11-11', '10:30:00',
# MAGIC  15, 10, 'Standard', 350.0, 'Completed', 'App'),
# MAGIC (9002, 'V902', 'A02', '2026-11-11', '11:00:00',
# MAGIC  25, 12, 'Express', 675.0, 'Completed', 'Web');

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM workspace.default.tp_entries_work
# MAGIC WHERE entry_id IN (9001, 9002);

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT entry_id, status, ticket_price
# MAGIC FROM workspace.default.tp_entries_work
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC UPDATE workspace.default.tp_entries_work
# MAGIC SET
# MAGIC     status = 'Completed',
# MAGIC     ticket_price = 400.0
# MAGIC WHERE entry_id = 1002;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM workspace.default.tp_entries_work
# MAGIC WHERE entry_id = 1002;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT entry_id, status
# MAGIC FROM workspace.default.tp_entries_work
# MAGIC WHERE status = 'Cancelled';

# COMMAND ----------

# MAGIC %sql
# MAGIC DELETE FROM workspace.default.tp_entries_work
# MAGIC WHERE entry_id = 1001
# MAGIC AND status = 'Cancelled';

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE EXTENDED workspace.default.tp_entries_work;

# COMMAND ----------

SECTION E

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT c.*
# MAGIC FROM workspace.default.tp_entry_changes c
# MAGIC INNER JOIN workspace.default.tp_entries_work w
# MAGIC ON c.entry_id = w.entry_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT c.*
# MAGIC FROM workspace.default.tp_entry_changes c
# MAGIC LEFT ANTI JOIN workspace.default.tp_entries_work w
# MAGIC ON c.entry_id = w.entry_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC MERGE INTO workspace.default.tp_entries_work AS target
# MAGIC USING workspace.default.tp_entry_changes AS source
# MAGIC ON target.entry_id = source.entry_id
# MAGIC
# MAGIC WHEN MATCHED THEN UPDATE SET
# MAGIC     target.visitor_id = source.visitor_id,
# MAGIC     target.attraction_id = source.attraction_id,
# MAGIC     target.visit_date = source.visit_date,
# MAGIC     target.entry_time = source.entry_time,
# MAGIC     target.wait_minutes = source.wait_minutes,
# MAGIC     target.ride_minutes = source.ride_minutes,
# MAGIC     target.ticket_type = source.ticket_type,
# MAGIC     target.ticket_price = source.ticket_price,
# MAGIC     target.status = source.status,
# MAGIC     target.booking_channel = source.booking_channel
# MAGIC
# MAGIC WHEN NOT MATCHED THEN INSERT (
# MAGIC     entry_id,
# MAGIC     visitor_id,
# MAGIC     attraction_id,
# MAGIC     visit_date,
# MAGIC     entry_time,
# MAGIC     wait_minutes,
# MAGIC     ride_minutes,
# MAGIC     ticket_type,
# MAGIC     ticket_price,
# MAGIC     status,
# MAGIC     booking_channel
# MAGIC )
# MAGIC VALUES (
# MAGIC     source.entry_id,
# MAGIC     source.visitor_id,
# MAGIC     source.attraction_id,
# MAGIC     source.visit_date,
# MAGIC     source.entry_time,
# MAGIC     source.wait_minutes,
# MAGIC     source.ride_minutes,
# MAGIC     source.ticket_type,
# MAGIC     source.ticket_price,
# MAGIC     source.status,
# MAGIC     source.booking_channel
# MAGIC );

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     c.entry_id,
# MAGIC     CASE
# MAGIC         WHEN w.entry_id IS NOT NULL
# MAGIC         THEN 'Present after MERGE'
# MAGIC         ELSE 'Missing'
# MAGIC     END AS merge_result
# MAGIC FROM workspace.default.tp_entry_changes c
# MAGIC LEFT JOIN workspace.default.tp_entries_work w
# MAGIC ON c.entry_id = w.entry_id
# MAGIC ORDER BY c.entry_id;

# COMMAND ----------

from delta.tables import DeltaTable
spark.table("workspace.default.tp_entries_backup") \
    .write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("workspace.default.tp_entries_work_api")
target_table = DeltaTable.forName(
    spark,
    "workspace.default.tp_entries_work_api"
)
source_df = spark.table(
    "workspace.default.tp_entry_changes"
)
target_table.alias("target").merge(
    source_df.alias("source"),
    "target.entry_id = source.entry_id"
).whenMatchedUpdateAll() \
 .whenNotMatchedInsertAll() \
 .execute()
display(
    spark.table("workspace.default.tp_entries_work_api")
)

# COMMAND ----------

attractions_df.printSchema()

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE workspace.default.tp_capacity_history
# MAGIC USING DELTA
# MAGIC AS
# MAGIC SELECT
# MAGIC     attraction_id,
# MAGIC     attraction_name,
# MAGIC     capacity_per_hour,
# MAGIC     CURRENT_DATE() AS valid_from,
# MAGIC     CAST(NULL AS DATE) AS valid_to,
# MAGIC     TRUE AS is_current
# MAGIC FROM workspace.default.tp_attractions;

# COMMAND ----------

# MAGIC %sql
# MAGIC UPDATE workspace.default.tp_capacity_history
# MAGIC SET
# MAGIC     valid_to = CURRENT_DATE(),
# MAGIC     is_current = FALSE
# MAGIC WHERE attraction_id = 'A01'
# MAGIC AND is_current = TRUE;

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO workspace.default.tp_capacity_history
# MAGIC (
# MAGIC     attraction_id,
# MAGIC     attraction_name,
# MAGIC     capacity_per_hour,
# MAGIC     valid_from,
# MAGIC     valid_to,
# MAGIC     is_current
# MAGIC )
# MAGIC VALUES
# MAGIC (
# MAGIC     'A01',
# MAGIC     'Sky Spinner',
# MAGIC     160,
# MAGIC     CURRENT_DATE(),
# MAGIC     NULL,
# MAGIC     TRUE
# MAGIC );

# COMMAND ----------

# MAGIC %md
# MAGIC SECTION E

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE DETAIL workspace.default.tp_entries_work;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY workspace.default.tp_entries_work;

# COMMAND ----------

history_df = spark.sql(
    "DESCRIBE HISTORY workspace.default.tp_entries_work"
)
display(history_df)
merge_history = history_df.filter(
    F.col("operation") == "MERGE"
).orderBy(
    F.col("version").desc()
).first()
if merge_history is None:
    raise Exception("MERGE operation not found")
merge_version = merge_history["version"]
pre_merge_version = merge_version - 1
print("MERGE version:", merge_version)
print("Previous version:", pre_merge_version)
before_merge_df = spark.sql(
    f"""
    SELECT *
    FROM workspace.default.tp_entries_work
    VERSION AS OF {pre_merge_version}
    """
)
display(before_merge_df)

# COMMAND ----------

compare_entry_id = 1003
before_df = spark.sql(
    f"""
    SELECT *
    FROM workspace.default.tp_entries_work
    VERSION AS OF {pre_merge_version}
    WHERE entry_id = {compare_entry_id}
    """
)
after_df = spark.sql(
    f"""
    SELECT *
    FROM workspace.default.tp_entries_work
    WHERE entry_id = {compare_entry_id}
    """
)
print("Before MERGE")
display(before_df)
print("After MERGE")
display(after_df)

# COMMAND ----------

# DBTITLE 1,Cell 53
detail_before = spark.sql(
    "DESCRIBE DETAIL workspace.default.tp_entries_work"
)
before_file_count = detail_before.first()["numFiles"]
print("Files before OPTIMIZE:", before_file_count)
spark.sql(
    "OPTIMIZE workspace.default.tp_entries_work"
)
detail_after = spark.sql(
    "DESCRIBE DETAIL workspace.default.tp_entries_work"
)
after_file_count = detail_after.first()["numFiles"]
print("Files after OPTIMIZE:", after_file_count)

# COMMAND ----------

# MAGIC %sql
# MAGIC OPTIMIZE workspace.default.tp_entries_work
# MAGIC ZORDER BY (attraction_id);

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY workspace.default.tp_entries_work;

# COMMAND ----------

# MAGIC %sql
# MAGIC VACUUM workspace.default.tp_entries_work DRY RUN;

# COMMAND ----------

# MAGIC %md
# MAGIC SECTION G

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE VIEW workspace.default.tp_completed_entries_view AS
# MAGIC SELECT
# MAGIC     e.entry_id,
# MAGIC     e.attraction_id,
# MAGIC     a.attraction_name,
# MAGIC     e.visit_date,
# MAGIC     e.ticket_type,
# MAGIC     e.ticket_price,
# MAGIC     e.wait_minutes
# MAGIC FROM workspace.default.tp_entries_work e
# MAGIC INNER JOIN workspace.default.tp_attractions a
# MAGIC ON e.attraction_id = a.attraction_id
# MAGIC WHERE e.status = 'Completed'
# MAGIC AND e.ticket_price > 0
# MAGIC AND e.wait_minutes >= 0;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM workspace.default.tp_completed_entries_view;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMP VIEW tp_long_wait_entries AS
# MAGIC SELECT *
# MAGIC FROM workspace.default.tp_entries_work
# MAGIC WHERE wait_minutes > 45;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM tp_long_wait_entries;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMP VIEW tp_global_entries AS
# MAGIC SELECT *
# MAGIC FROM workspace.default.tp_entries_work;

# COMMAND ----------

parquet_path = (
    "/Volumes/workspace/default/themepark_files/parquet_output/tp_entries_parquet"
)
clean_entries_df.write \
    .format("parquet") \
    .mode("overwrite") \
    .save(parquet_path)
parquet_df = spark.read \
    .format("parquet") \
    .load(parquet_path)
parquet_df.printSchema()
print("Parquet rows:", parquet_df.count())
display(parquet_df)

# COMMAND ----------

# MAGIC %md
# MAGIC SECTION H

# COMMAND ----------


for query in spark.streams.active:
    print("Stopping:", query.name)
    query.stop()


# COMMAND ----------

from pyspark.sql import functions as F
rate_df = spark.readStream \
    .format("rate") \
    .option("rowsPerSecond", 5) \
    .load()
rate_df.printSchema()

# COMMAND ----------

from pyspark.sql import functions as F
transformed_stream = (rate_df
                      .withColumn("visitor_event_id", F.concat(F.lit("EVT-"), F.col("value")))
                      .withColumn("simulated_wait_minutes", (F.rand(seed=42) * 60).cast("int")))

# COMMAND ----------

filtered_stream = transformed_stream.filter(F.col("simulated_wait_minutes") > 30)

# COMMAND ----------

# DBTITLE 1,Cell 69
aggregated_stream = (filtered_stream
                     .withColumn("wait_category", 
                                 F.when(F.col("simulated_wait_minutes") <= 45, "Medium")
                                  .otherwise("Long"))
                     .groupBy("wait_category")
                     .count())
active_query = (aggregated_stream.writeStream
                .format("memory")
                .queryName("streaming_wait_counts")
                .outputMode("complete")
                .trigger(availableNow=True)
                .option("checkpointLocation", "/Volumes/workspace/default/themepark_files/checkpoints/streaming_wait_counts")
                .start())
active_query.stop()

# COMMAND ----------

# MAGIC %md
# MAGIC SECTION I

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REFRESH STREAMING TABLE pipeline_bronze_entries
# MAGIC COMMENT "Bronze ingest mapping append-only raw theme park logs."
# MAGIC AS SELECT 
# MAGIC   *,
# MAGIC   _metadata.file_name AS source_file,
# MAGIC   current_timestamp() AS ingest_time
# MAGIC FROM STREAM(LIVE.tp_entries_raw);

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REFRESH STREAMING TABLE pipeline_silver_entries(
# MAGIC   CONSTRAINT valid_ticket_price EXPECT (ticket_price >= 0) ON VIOLATION DROP ROW,
# MAGIC   CONSTRAINT positive_wait_times EXPECT (wait_minutes >= 0) ON VIOLATION DROP ROW
# MAGIC )
# MAGIC COMMENT "Silver cleaned and filtered core dataset for visitor telemetry."
# MAGIC AS SELECT
# MAGIC   CAST(entry_id AS INT) as entry_id,
# MAGIC   visitor_id,
# MAGIC   attraction_id,
# MAGIC   CAST(visit_date AS DATE) as visit_date,
# MAGIC   to_timestamp(concat(visit_date, ' ', entry_time)) as entry_timestamp,
# MAGIC   CAST(wait_minutes AS INT) as wait_minutes,
# MAGIC   CAST(ride_minutes AS INT) as ride_minutes,
# MAGIC   ticket_type,
# MAGIC   CAST(ticket_price AS DECIMAL(10,2)) as ticket_price,
# MAGIC   status,
# MAGIC   COALESCE(booking_channel, 'Unknown') as booking_channel
# MAGIC FROM STREAM(LIVE.pipeline_bronze_entries)
# MAGIC WHERE status = 'Completed';

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REFRESH MATERIALIZED VIEW pipeline_gold_attraction_analytics
# MAGIC COMMENT "Gold domain metrics breaking down attendance statistics and financial yields."
# MAGIC AS SELECT 
# MAGIC   a.attraction_id,
# MAGIC   a.attraction_name,
# MAGIC   a.category,
# MAGIC   COUNT(s.entry_id) as total_entries,
# MAGIC   SUM(s.ticket_price) as total_revenue,
# MAGIC   AVG(s.wait_minutes) as average_wait_minutes
# MAGIC FROM LIVE.pipeline_silver_entries s
# MAGIC JOIN LIVE.tp_attractions a ON s.attraction_id = a.attraction_id
# MAGIC GROUP BY a.attraction_id, a.attraction_name, a.category;

# COMMAND ----------

from pyspark.sql.functions import (
    count, sum, avg, round, col
)
entries = spark.table(
    "workspace.default.tp_entries_raw"
)
attractions = spark.table(
    "workspace.default.tp_attractions"
)
completed = entries.filter(
    col("status") == "Completed"
)
print("Total Entries:", entries.count())
print("Completed Entries:", completed.count())
print("Total Revenue:")
completed.agg(
    round(sum("ticket_price"), 2).alias("total_revenue")
).show()
print("Average Waiting Time:")
completed.agg(
    round(avg("wait_minutes"), 2).alias("average_wait")
).show()

# COMMAND ----------

df_inc = (spark.read.csv("/Volumes/workspace/default/themepark_files/park_entries_incremental.csv", 
                         header=True, inferSchema=True))
df_inc.write.mode("append").saveAsTable("tp_entries_raw")

# COMMAND ----------

# MAGIC %md
# MAGIC FINAL CAPSTONE PROJECT

# COMMAND ----------

bronze_df = spark.table(
    "workspace.default.tp_entries_raw"
)
print("Bronze records:", bronze_df.count())
display(bronze_df)

# COMMAND ----------

silver_df = (
    bronze_df
    .filter(
        (F.col("ticket_price") > 0) &
        (F.col("wait_minutes") >= 0) &
        (F.col("ride_minutes") > 0) &
        F.col("attraction_id").isNotNull()
    )
    .fillna({"booking_channel": "Unknown"})
    .dropDuplicates(["entry_id"])
    .withColumn(
        "visit_date",
        F.to_date("visit_date", "yyyy-MM-dd")
    )
    .withColumn(
        "ticket_revenue",
        F.col("ticket_price")
    )
)

display(silver_df)


# COMMAND ----------

gold_df = silver_df.join(
    attractions_df,
    on="attraction_id",
    how="inner"
).groupBy(
    "attraction_id",
    "attraction_name",
    F.col("location.zone").alias("zone")
).agg(
    F.count("*").alias("total_entries"),
    F.sum("ticket_revenue").alias("total_revenue"),
    F.round(
        F.avg("wait_minutes"), 2
    ).alias("average_wait_minutes")
)
display(gold_df)

# COMMAND ----------

gold_df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("workspace.default.tp_park_gold")

# COMMAND ----------

revenue_chart_df = gold_df.select(
    "attraction_name",
    "total_revenue"
).orderBy("total_revenue", ascending=False)
display(revenue_chart_df)

# COMMAND ----------

ticket_share_df = silver_df.groupBy(
    "ticket_type"
).agg(
    F.count("*").alias("total_tickets")
)
display(ticket_share_df)

# COMMAND ----------

daily_revenue_df = silver_df.groupBy(
    "visit_date"
).agg(
    F.sum("ticket_revenue").alias("daily_revenue")
).orderBy("visit_date")
display(daily_revenue_df)

# COMMAND ----------

scatter_chart_df = gold_df.select(
    "attraction_name",
    "average_wait_minutes",
    "total_revenue"
)
display(scatter_chart_df)

# COMMAND ----------

display(
    gold_df.orderBy(
        F.col("total_revenue").desc()
    ).limit(5)
)
display(
    gold_df.orderBy(
        F.col("average_wait_minutes").desc()
    ).limit(5)
)
print("Total revenue:", gold_df.agg(
    F.sum("total_revenue")
).first()[0])
print("Total entries:", gold_df.agg(
    F.sum("total_entries")
).first()[0])