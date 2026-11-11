# Databricks notebook source
# MAGIC %md
# MAGIC SECTION A

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE water_meter_readings_source;
# MAGIC SELECT COUNT(*) AS total_rows
# MAGIC FROM water_meter_readings_source;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     reading_id,
# MAGIC     meter_id,
# MAGIC     zone_id,
# MAGIC     reading_time,
# MAGIC     consumption_liters
# MAGIC FROM water_meter_readings_source
# MAGIC WHERE reading_status = 'Valid';

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM water_meter_readings_source
# MAGIC WHERE pressure_bar < 2.5
# MAGIC ORDER BY pressure_bar ASC;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM water_meter_readings_source
# MAGIC WHERE flow_lpm BETWEEN 20 AND 50
# MAGIC AND source_system IN ('Gateway', 'SmartMeter');

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     reading_status,
# MAGIC     COUNT(*) AS reading_count
# MAGIC FROM water_meter_readings_source
# MAGIC GROUP BY reading_status
# MAGIC ORDER BY reading_count DESC;

# COMMAND ----------

# MAGIC %md
# MAGIC SECTION B

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     z.zone_name,
# MAGIC     z.district,
# MAGIC     r.meter_id,
# MAGIC     r.consumption_liters
# MAGIC FROM water_meter_readings_source r
# MAGIC INNER JOIN water_zones z
# MAGIC ON r.zone_id = z.zone_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT r.*
# MAGIC FROM water_meter_readings_source r
# MAGIC LEFT JOIN water_zones z
# MAGIC ON r.zone_id = z.zone_id
# MAGIC WHERE z.zone_id IS NULL;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     z.zone_id,
# MAGIC     z.zone_name,
# MAGIC     z.district
# MAGIC FROM water_zones z
# MAGIC LEFT JOIN water_meter_readings_source r
# MAGIC ON z.zone_id = r.zone_id
# MAGIC WHERE r.zone_id IS NULL;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     zone_id,
# MAGIC     SUM(consumption_liters) AS total_valid_consumption,
# MAGIC     AVG(pressure_bar) AS average_pressure,
# MAGIC     COUNT(*) AS reading_count
# MAGIC FROM water_meter_readings_source
# MAGIC WHERE reading_status = 'Valid'
# MAGIC AND consumption_liters > 0
# MAGIC GROUP BY zone_id
# MAGIC ORDER BY total_valid_consumption DESC;

# COMMAND ----------

# DBTITLE 1,Cell 12
# MAGIC %sql
# MAGIC WITH meter_totals AS (
# MAGIC     SELECT
# MAGIC         z.district,
# MAGIC         r.meter_id,
# MAGIC         SUM(r.consumption_liters) AS total_consumption
# MAGIC     FROM water_meter_readings_source r
# MAGIC     INNER JOIN water_zones z
# MAGIC     ON r.zone_id = z.zone_id
# MAGIC     WHERE r.reading_status = 'Valid'
# MAGIC     AND r.consumption_liters > 0
# MAGIC     GROUP BY z.district, r.meter_id
# MAGIC )
# MAGIC SELECT
# MAGIC     district,
# MAGIC     meter_id,
# MAGIC     total_consumption,
# MAGIC     RANK() OVER (
# MAGIC         PARTITION BY district
# MAGIC         ORDER BY total_consumption DESC
# MAGIC     ) AS consumption_rank
# MAGIC FROM meter_totals;

# COMMAND ----------

# MAGIC %md
# MAGIC SECTION C

# COMMAND ----------

readings_df = spark.table("water_meter_readings_source")
zones_df = spark.table("water_zones")
readings_df.printSchema()
zones_df.printSchema()

# COMMAND ----------

from pyspark.sql.functions import col
high_flow_df = readings_df.select(
    "reading_id",
    "meter_id",
    "zone_id",
    "flow_lpm",
    "reading_status"
).filter(
    (col("flow_lpm") >= 60) &
    (col("reading_status") == "Valid")
).orderBy(
    col("flow_lpm").desc()
)
high_flow_df.show(truncate=False)

# COMMAND ----------

from pyspark.sql.functions import when, col
categorized_df = readings_df.withColumn(
    "flow_category",
    when(col("flow_lpm").isNull(), "Unknown")
    .when(col("flow_lpm") >= 60, "High")
    .when(col("flow_lpm") >= 30, "Medium")
    .otherwise("Low")
)
categorized_df.show(truncate=False)

# COMMAND ----------

from pyspark.sql.functions import avg
joined_df = readings_df.join(
    zones_df,
    readings_df.zone_id == zones_df.zone_id,
    "inner"
)
zone_type_avg_df = joined_df.groupBy(
    "zone_type"
).agg(
    avg("flow_lpm").alias("average_flow_lpm")
)
zone_type_avg_df.show()

# COMMAND ----------

from pyspark.sql.functions import sum, col
top_zones_df = readings_df.filter(
    (col("reading_status") == "Valid") &
    (col("consumption_liters") > 0)
).groupBy(
    "zone_id"
).agg(
    sum("consumption_liters").alias("total_consumption")
).orderBy(
    col("total_consumption").desc()
).limit(3)
top_zones_df.show()

# COMMAND ----------

# MAGIC %md
# MAGIC SECTION D

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     reading_id,
# MAGIC     COUNT(*) AS duplicate_count
# MAGIC FROM water_meter_readings_source
# MAGIC GROUP BY reading_id
# MAGIC HAVING COUNT(*) > 1;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM water_meter_readings_source
# MAGIC WHERE reading_id IN (
# MAGIC     SELECT reading_id
# MAGIC     FROM water_meter_readings_source
# MAGIC     GROUP BY reading_id
# MAGIC     HAVING COUNT(*) > 1
# MAGIC )
# MAGIC ORDER BY reading_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     COUNT(CASE WHEN pressure_bar IS NULL THEN 1 END)
# MAGIC         AS missing_pressure_count,
# MAGIC     COUNT(CASE WHEN source_system IS NULL THEN 1 END)
# MAGIC         AS missing_source_count,
# MAGIC     COUNT(CASE
# MAGIC         WHEN pressure_bar IS NULL OR source_system IS NULL
# MAGIC         THEN 1
# MAGIC     END) AS total_affected_records
# MAGIC FROM water_meter_readings_source;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM water_meter_readings_source
# MAGIC WHERE flow_lpm < 0
# MAGIC    OR consumption_liters <= 0
# MAGIC    OR zone_id IS NULL;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE water_readings_clean
# MAGIC USING DELTA
# MAGIC AS
# MAGIC SELECT *
# MAGIC FROM (
# MAGIC     SELECT
# MAGIC         *,
# MAGIC         ROW_NUMBER() OVER (
# MAGIC             PARTITION BY reading_id
# MAGIC             ORDER BY
# MAGIC                 reading_time DESC NULLS LAST,
# MAGIC                 meter_id ASC NULLS LAST,
# MAGIC                 zone_id ASC NULLS LAST,
# MAGIC                 flow_lpm DESC NULLS LAST,
# MAGIC                 pressure_bar DESC NULLS LAST,
# MAGIC                 consumption_liters DESC NULLS LAST
# MAGIC         ) AS row_num
# MAGIC     FROM water_meter_readings_source
# MAGIC     WHERE reading_status = 'Valid'
# MAGIC       AND flow_lpm > 0
# MAGIC       AND consumption_liters > 0
# MAGIC       AND zone_id IS NOT NULL
# MAGIC ) cleaned
# MAGIC WHERE row_num = 1;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     s.zone_id,
# MAGIC     COUNT(s.request_id) AS high_priority_requests,
# MAGIC     AVG(r.pressure_bar) AS average_pressure
# MAGIC FROM water_service_requests s
# MAGIC LEFT JOIN water_readings_clean r
# MAGIC     ON s.zone_id = r.zone_id
# MAGIC WHERE s.priority = 'High'
# MAGIC GROUP BY s.zone_id
# MAGIC ORDER BY high_priority_requests DESC;

# COMMAND ----------

# MAGIC %md
# MAGIC SECTION E

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE water_readings_work_copy
# MAGIC USING DELTA
# MAGIC AS
# MAGIC SELECT *
# MAGIC FROM water_meter_readings_work;

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO water_readings_work_copy
# MAGIC (
# MAGIC     reading_id,
# MAGIC     meter_id,
# MAGIC     zone_id,
# MAGIC     reading_time,
# MAGIC     flow_lpm,
# MAGIC     pressure_bar,
# MAGIC     chlorine_mg_l,
# MAGIC     consumption_liters,
# MAGIC     reading_status,
# MAGIC     source_system
# MAGIC )
# MAGIC VALUES
# MAGIC (
# MAGIC     9001,
# MAGIC     'M9001',
# MAGIC     'W01',
# MAGIC     TIMESTAMP '2026-10-21 10:00:00',
# MAGIC     45.5,
# MAGIC     3.2,
# MAGIC     0.5,
# MAGIC     120,
# MAGIC     'Valid',
# MAGIC     'SmartMeter'
# MAGIC ),
# MAGIC (
# MAGIC     9002,
# MAGIC     'M9002',
# MAGIC     'W02',
# MAGIC     TIMESTAMP '2026-10-21 11:00:00',
# MAGIC     52.0,
# MAGIC     3.0,
# MAGIC     0.6,
# MAGIC     150,
# MAGIC     'Valid',
# MAGIC     'Gateway'
# MAGIC );

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT reading_id, reading_status
# MAGIC FROM water_readings_work_copy
# MAGIC WHERE reading_status = 'Suspect'
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC UPDATE water_readings_work_copy
# MAGIC SET reading_status = 'Rejected'
# MAGIC WHERE reading_id = 1090
# MAGIC AND reading_status = 'Suspect';

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT reading_id, reading_status
# MAGIC FROM water_readings_work_copy
# MAGIC WHERE reading_id = 1090;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS count_before
# MAGIC FROM water_readings_work_copy;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS rejected_count
# MAGIC FROM water_readings_work_copy
# MAGIC WHERE reading_status = 'Rejected';

# COMMAND ----------

# MAGIC %sql
# MAGIC DELETE FROM water_readings_work_copy
# MAGIC WHERE reading_status = 'Rejected';

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS count_after
# MAGIC FROM water_readings_work_copy;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS remaining_rejected
# MAGIC FROM water_readings_work_copy
# MAGIC WHERE reading_status = 'Rejected';

# COMMAND ----------

from pyspark.sql.functions import sum, avg, count, col
readings_df = spark.table("water_readings_clean")
zone_consumption_df = readings_df.groupBy(
    "zone_id"
).agg(
    sum("consumption_liters").alias("total_consumption"),
    avg("pressure_bar").alias("average_pressure"),
    avg("flow_lpm").alias("average_flow"),
    count("*").alias("reading_count")
)
zone_consumption_df.write.format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("zone_consumption_summary")
display(spark.table("zone_consumption_summary"))

# COMMAND ----------

# MAGIC %md
# MAGIC SECTION F

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     c.reading_id,
# MAGIC     'MATCHED' AS record_type
# MAGIC FROM water_reading_changes c
# MAGIC INNER JOIN water_meter_readings_work w
# MAGIC ON c.reading_id = w.reading_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     c.reading_id,
# MAGIC     'NEW' AS record_type
# MAGIC FROM water_reading_changes c
# MAGIC LEFT ANTI JOIN water_meter_readings_work w
# MAGIC ON c.reading_id = w.reading_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     COUNT(*) AS total_change_records,
# MAGIC     COUNT(CASE WHEN w.reading_id IS NOT NULL THEN 1 END)
# MAGIC         AS matching_records,
# MAGIC     COUNT(CASE WHEN w.reading_id IS NULL THEN 1 END)
# MAGIC         AS new_records
# MAGIC FROM water_reading_changes c
# MAGIC LEFT JOIN water_meter_readings_work w
# MAGIC ON c.reading_id = w.reading_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC MERGE INTO water_meter_readings_work AS target
# MAGIC USING water_reading_changes AS source
# MAGIC ON target.reading_id = source.reading_id
# MAGIC WHEN MATCHED THEN
# MAGIC     UPDATE SET *
# MAGIC WHEN NOT MATCHED THEN
# MAGIC     INSERT *;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     w.reading_id,
# MAGIC     w.meter_id,
# MAGIC     w.flow_lpm,
# MAGIC     w.pressure_bar,
# MAGIC     w.consumption_liters,
# MAGIC     w.reading_status
# MAGIC FROM water_meter_readings_work w
# MAGIC INNER JOIN water_reading_changes c
# MAGIC ON w.reading_id = c.reading_id
# MAGIC ORDER BY w.reading_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     COUNT(*) AS records_found
# MAGIC FROM water_reading_changes c
# MAGIC INNER JOIN water_meter_readings_work w
# MAGIC ON c.reading_id = w.reading_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM water_meter_readings_work
# MAGIC WHERE reading_id BETWEEN 1201 AND 1206;

# COMMAND ----------

from delta.tables import DeltaTable
spark.sql("""
CREATE OR REPLACE TABLE water_meter_readings_pyspark_copy
USING DELTA
AS
SELECT *
FROM water_meter_readings_source
""")

# COMMAND ----------

target_df = DeltaTable.forName(
    spark,
    "water_meter_readings_pyspark_copy"
)
changes_df = spark.table("water_reading_changes")

# COMMAND ----------

target_df.alias("target").merge(
    changes_df.alias("source"),
    "target.reading_id = source.reading_id"
).whenMatchedUpdateAll(
).whenNotMatchedInsertAll(
).execute()

# COMMAND ----------

result_df = spark.table(
    "water_meter_readings_pyspark_copy"
)
print("Total rows:", result_df.count())
display(
    result_df.orderBy("reading_id")
)

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE zone_capacity_history
# MAGIC USING DELTA
# MAGIC AS
# MAGIC SELECT
# MAGIC     zone_id,
# MAGIC     zone_name,
# MAGIC     city,
# MAGIC     district,
# MAGIC     zone_type,
# MAGIC     daily_capacity_liters,
# MAGIC     active,
# MAGIC     commissioned_on,
# MAGIC     DATE '2026-10-20' AS effective_start_date,
# MAGIC     CAST(NULL AS DATE) AS effective_end_date,
# MAGIC     TRUE AS is_current
# MAGIC FROM water_zones;

# COMMAND ----------

# MAGIC %sql
# MAGIC UPDATE zone_capacity_history
# MAGIC SET
# MAGIC     effective_end_date = DATE '2026-10-19',
# MAGIC     is_current = FALSE
# MAGIC WHERE zone_id IN ('W02', 'W06')
# MAGIC AND is_current = TRUE;

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO zone_capacity_history
# MAGIC (
# MAGIC     zone_id,
# MAGIC     zone_name,
# MAGIC     city,
# MAGIC     district,
# MAGIC     zone_type,
# MAGIC     daily_capacity_liters,
# MAGIC     active,
# MAGIC     commissioned_on,
# MAGIC     effective_start_date,
# MAGIC     effective_end_date,
# MAGIC     is_current
# MAGIC )
# MAGIC SELECT
# MAGIC     zone_id,
# MAGIC     zone_name,
# MAGIC     city,
# MAGIC     district,
# MAGIC     zone_type,
# MAGIC     CASE
# MAGIC         WHEN zone_id = 'W02' THEN 195000
# MAGIC         WHEN zone_id = 'W06' THEN 305000
# MAGIC     END AS daily_capacity_liters,
# MAGIC     active,
# MAGIC     commissioned_on,
# MAGIC     DATE '2026-10-20',
# MAGIC     CAST(NULL AS DATE),
# MAGIC     TRUE
# MAGIC FROM water_zones
# MAGIC WHERE zone_id IN ('W02', 'W06');

# COMMAND ----------

# MAGIC %md
# MAGIC SECTION G

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE DETAIL water_meter_readings_work;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY water_meter_readings_work;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM water_meter_readings_work
# MAGIC VERSION AS OF 1
# MAGIC WHERE reading_id = 1005;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM water_meter_readings_work
# MAGIC WHERE reading_id = 1005;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE DETAIL water_meter_readings_work;

# COMMAND ----------

# MAGIC %sql
# MAGIC OPTIMIZE water_meter_readings_work;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE DETAIL water_meter_readings_work;

# COMMAND ----------

# MAGIC %sql
# MAGIC VACUUM water_meter_readings_work DRY RUN;

# COMMAND ----------

# MAGIC %md
# MAGIC SECTION H

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     current_catalog() AS catalog_name,
# MAGIC     current_schema() AS schema_name;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE DETAIL water_meter_readings_work;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE VIEW valid_readings_with_zone AS
# MAGIC SELECT
# MAGIC     r.reading_id,
# MAGIC     r.meter_id,
# MAGIC     r.zone_id,
# MAGIC     z.zone_name,
# MAGIC     z.district,
# MAGIC     r.reading_time,
# MAGIC     r.flow_lpm,
# MAGIC     r.pressure_bar,
# MAGIC     r.chlorine_mg_l,
# MAGIC     r.consumption_liters
# MAGIC FROM water_readings_clean r
# MAGIC LEFT JOIN water_zones z
# MAGIC ON r.zone_id = z.zone_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM valid_readings_with_zone;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMP VIEW low_pressure_readings AS
# MAGIC SELECT *
# MAGIC FROM water_meter_readings_source
# MAGIC WHERE pressure_bar < 2.5;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM low_pressure_readings
# MAGIC ORDER BY pressure_bar;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE VIEW high_priority_requests AS
# MAGIC SELECT *
# MAGIC FROM water_service_requests
# MAGIC WHERE priority = 'High';

# COMMAND ----------

# DBTITLE 1,Cell 70
# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM workspace.default.high_priority_requests;

# COMMAND ----------

readings_df = spark.table("water_readings_clean")

# COMMAND ----------

parquet_path = "/Volumes/workspace/default/citywater_files/water_network/parquet_exports/water_readings_clean"

# COMMAND ----------

readings_df.write \
    .mode("overwrite") \
    .parquet(parquet_path)

# COMMAND ----------

parquet_df = spark.read.parquet(parquet_path)
parquet_df.printSchema()
display(parquet_df)

# COMMAND ----------

parquet_df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("water_readings_from_parquet")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*)
# MAGIC FROM water_readings_from_parquet;

# COMMAND ----------

# MAGIC %md
# MAGIC SECTION I

# COMMAND ----------

rate_df = spark.readStream \
    .format("rate") \
    .option("rowsPerSecond", 5) \
    .load()
rate_df.printSchema()

# COMMAND ----------

from pyspark.sql.functions import col, concat, lit, lpad
meter_stream_df = rate_df.withColumn(
    "meter_id",
    concat(
        lit("M"),
        lpad((col("value") % 100).cast("string"), 3, "0")
    )
).withColumn(
    "flow_lpm",
    ((col("value") * 7) % 80).cast("double")
)
display(meter_stream_df, checkpointLocation = "/Volumes/workspace/default/citywater_files/checkpoints/meter_stream_display")

# COMMAND ----------

filtered_stream_df = meter_stream_df.filter(
    col("flow_lpm") > 40
)
display(filtered_stream_df, checkpointLocation = "/Volumes/workspace/default/citywater_files/checkpoints/filtered_stream_display")

# COMMAND ----------

from pyspark.sql.functions import when, count
categorized_stream_df = filtered_stream_df.withColumn(
    "flow_category",
    when(col("flow_lpm") >= 60, "High")
    .when(col("flow_lpm") >= 30, "Medium")
    .otherwise("Low")
)

# COMMAND ----------

flow_count_df = categorized_stream_df.groupBy(
    "flow_category"
).agg(
    count("*").alias("total_readings")
)

# COMMAND ----------

# DBTITLE 1,Cell 83
streaming_query = flow_count_df.writeStream \
    .format("memory") \
    .queryName("water_flow_category_counts") \
    .outputMode("complete") \
    .option(
        "checkpointLocation",
        "/Volumes/workspace/default/citywater_files/water_network/checkpoints/water_flow_counts"
    ) \
    .trigger(availableNow=True) \
    .start()

# COMMAND ----------

display(
    spark.sql("""
        SELECT *
        FROM water_flow_category_counts
    """)
)

# COMMAND ----------

streaming_query.stop()

# COMMAND ----------

print("Streaming query active:", streaming_query.isActive)

# COMMAND ----------

from question 46-50 the pipeline name is 
1.water_pipeline.sql(question 46-49,52) 
2.pyspark.pipelines.py(question 50)

# COMMAND ----------

# MAGIC %md
# MAGIC SECTION K

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM water_readings_incremental_staging;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*)
# MAGIC FROM water_readings_incremental_staging;

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO water_meter_readings_source
# MAGIC SELECT i.*
# MAGIC FROM water_readings_incremental_staging i
# MAGIC LEFT ANTI JOIN water_meter_readings_source s
# MAGIC ON i.reading_id = s.reading_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*)
# MAGIC FROM water_meter_readings_source;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM water_meter_readings_source
# MAGIC WHERE reading_id BETWEEN 1161 AND 1178
# MAGIC ORDER BY reading_id;

# COMMAND ----------

from pyspark.sql.functions import sum, col
bar_chart_df = spark.table(
    "water_readings_clean"
).groupBy(
    "zone_id"
).agg(
    sum("consumption_liters").alias("total_consumption")
).orderBy(
    col("total_consumption").desc()
)
display(bar_chart_df)

# COMMAND ----------

district_chart_df = spark.table(
    "water_readings_clean"
).join(
    spark.table("water_zones"),
    "zone_id",
    "left"
).groupBy(
    "district"
).agg(
    sum("consumption_liters").alias("total_consumption")
).orderBy(
    col("total_consumption").desc()
)
display(district_chart_df)

# COMMAND ----------

from pyspark.sql.functions import to_date, sum, col
daily_consumption_df = spark.table(
    "water_readings_clean"
).groupBy(
    to_date("reading_time").alias("reading_date")
).agg(
    sum("consumption_liters").alias("daily_consumption")
).orderBy(
    "reading_date"
)
display(daily_consumption_df)

# COMMAND ----------

scatter_df = spark.table(
    "water_readings_clean"
).select(
    "pressure_bar",
    "flow_lpm"
).filter(
    col("pressure_bar").isNotNull() &
    col("flow_lpm").isNotNull()
)
display(scatter_df)

# COMMAND ----------

# MAGIC %sql
# MAGIC WITH consumption AS (
# MAGIC     SELECT
# MAGIC         zone_id,
# MAGIC         SUM(consumption_liters) AS total_consumption,
# MAGIC         COUNT(*) AS reading_count
# MAGIC     FROM water_readings_clean
# MAGIC     GROUP BY zone_id
# MAGIC ),
# MAGIC
# MAGIC quality AS (
# MAGIC     SELECT
# MAGIC         zone_id,
# MAGIC         AVG(pressure_bar) AS average_pressure,
# MAGIC         AVG(chlorine_mg_l) AS average_chlorine,
# MAGIC         COUNT(
# MAGIC             CASE WHEN pressure_bar < 2.5 THEN 1 END
# MAGIC         ) AS low_pressure_readings
# MAGIC     FROM water_readings_clean
# MAGIC     GROUP BY zone_id
# MAGIC ),
# MAGIC
# MAGIC requests AS (
# MAGIC     SELECT
# MAGIC         zone_id,
# MAGIC         COUNT(*) AS total_requests,
# MAGIC         COUNT(
# MAGIC             CASE WHEN priority = 'High' THEN 1 END
# MAGIC         ) AS high_priority_requests
# MAGIC     FROM water_service_requests
# MAGIC     GROUP BY zone_id
# MAGIC )
# MAGIC
# MAGIC SELECT
# MAGIC     z.zone_id,
# MAGIC     z.zone_name,
# MAGIC     z.district,
# MAGIC     COALESCE(c.total_consumption, 0) AS total_consumption,
# MAGIC     COALESCE(c.reading_count, 0) AS reading_count,
# MAGIC     q.average_pressure,
# MAGIC     q.average_chlorine,
# MAGIC     COALESCE(q.low_pressure_readings, 0)
# MAGIC         AS low_pressure_readings,
# MAGIC     COALESCE(r.total_requests, 0) AS total_requests,
# MAGIC     COALESCE(r.high_priority_requests, 0)
# MAGIC         AS high_priority_requests
# MAGIC FROM water_zones z
# MAGIC LEFT JOIN consumption c
# MAGIC     ON z.zone_id = c.zone_id
# MAGIC LEFT JOIN quality q
# MAGIC     ON z.zone_id = q.zone_id
# MAGIC LEFT JOIN requests r
# MAGIC     ON z.zone_id = r.zone_id
# MAGIC ORDER BY total_consumption DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC WITH ranked_readings AS (
# MAGIC     SELECT
# MAGIC         *,
# MAGIC         ROW_NUMBER() OVER (
# MAGIC             PARTITION BY reading_id
# MAGIC             ORDER BY reading_time DESC
# MAGIC         ) AS row_num
# MAGIC
# MAGIC     FROM bronze_water_readings
# MAGIC )
# MAGIC SELECT
# MAGIC     reading_id,
# MAGIC     meter_id,
# MAGIC     zone_id,
# MAGIC     reading_time,
# MAGIC     flow_lpm,
# MAGIC     pressure_bar,
# MAGIC     chlorine_mg_l,
# MAGIC     consumption_liters,
# MAGIC     reading_status,
# MAGIC     source_system
# MAGIC
# MAGIC FROM ranked_readings
# MAGIC WHERE row_num = 1
# MAGIC AND reading_status = 'Valid'
# MAGIC AND zone_id IS NOT NULL
# MAGIC AND flow_lpm > 0
# MAGIC AND consumption_liters > 0;