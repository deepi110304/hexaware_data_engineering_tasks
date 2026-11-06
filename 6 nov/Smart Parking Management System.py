# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE parking_sessions_source (
# MAGIC     session_id INT,
# MAGIC     zone_id STRING,
# MAGIC     vehicle_type STRING,
# MAGIC     duration_hours INT,
# MAGIC     parking_fee INT,
# MAGIC     status STRING
# MAGIC )
# MAGIC USING DELTA;

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO parking_sessions_source VALUES
# MAGIC (101, 'Z01', 'Car', 3, 150, 'Completed'),
# MAGIC (102, 'Z02', 'Bike', 2, 40, 'Completed'),
# MAGIC (103, 'Z03', 'Car', 5, 250, 'Completed'),
# MAGIC (104, 'Z01', 'SUV', 4, 240, 'Active'),
# MAGIC (105, 'Z04', 'Bike', 1, 20, 'Completed'),
# MAGIC (106, 'Z02', 'Car', 6, 300, 'Completed'),
# MAGIC (107, 'Z03', 'SUV', 2, 120, 'Cancelled'),
# MAGIC (108, 'Z05', 'Car', 3, 150, 'Completed'),
# MAGIC (109, 'Z01', 'Bike', 4, 80, 'Completed'),
# MAGIC (110, 'Z04', 'SUV', 5, 300, 'Active'),
# MAGIC (111, 'Z02', 'Car', 2, 100, 'Completed'),
# MAGIC (112, 'Z05', 'Bike', 3, 60, 'Cancelled'),
# MAGIC (113, 'Z03', 'Car', 7, 350, 'Completed'),
# MAGIC (114, 'Z01', 'SUV', 3, 180, 'Completed'),
# MAGIC (115, 'Z04', 'Bike', 2, 40, 'Active'),
# MAGIC (116, 'Z05', 'Car', 4, 200, 'Completed'),
# MAGIC (117, 'Z02', 'SUV', 6, 360, 'Completed'),
# MAGIC (118, 'Z03', 'Bike', 1, 20, 'Completed'),
# MAGIC (119, 'Z04', 'Car', 5, 250, 'Completed'),
# MAGIC (120, 'Z05', 'SUV', 2, 120, 'Active');

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE parking_sessions_work
# MAGIC USING DELTA
# MAGIC AS
# MAGIC SELECT * FROM parking_sessions_source;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE parking_zones (
# MAGIC     zone_id STRING,
# MAGIC     zone_name STRING,
# MAGIC     city STRING,
# MAGIC     capacity INT
# MAGIC )
# MAGIC USING DELTA;

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO parking_zones VALUES
# MAGIC ('Z01', 'Central Plaza', 'Hyderabad', 100),
# MAGIC ('Z02', 'Metro Parking', 'Bengaluru', 150),
# MAGIC ('Z03', 'City Mall', 'Mumbai', 200),
# MAGIC ('Z04', 'Airport Parking', 'Delhi', 250),
# MAGIC ('Z05', 'Tech Park', 'Pune', 120);

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMP VIEW incoming_parking_sessions AS
# MAGIC SELECT *
# MAGIC FROM VALUES
# MAGIC (102, 'Z02', 'Bike', 3, 60, 'Completed'),
# MAGIC (104, 'Z01', 'SUV', 5, 300, 'Completed'),
# MAGIC (121, 'Z03', 'Car', 4, 200, 'Completed'),
# MAGIC (122, 'Z05', 'Bike', 2, 40, 'Active')
# MAGIC AS t(
# MAGIC     session_id,
# MAGIC     zone_id,
# MAGIC     vehicle_type,
# MAGIC     duration_hours,
# MAGIC     parking_fee,
# MAGIC     status
# MAGIC );

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT session_id, vehicle_type, parking_fee FROM parking_sessions_source;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM parking_sessions_source WHERE status = 'Completed' AND parking_fee > 100; 

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC     vehicle_type, 
# MAGIC     SUM(parking_fee) AS total_parking_fees,
# MAGIC     COUNT(session_id) AS total_sessions_count
# MAGIC FROM parking_sessions_source 
# MAGIC WHERE status = 'Completed'
# MAGIC GROUP BY vehicle_type;

# COMMAND ----------

from pyspark.sql.functions import col, when
df_source = spark.read.table("parking_sessions_source")
df_transformed = df_source.withColumn(
    "fee_category", 
    when(col("parking_fee") >= 200, "High").otherwise("Low")
)

display(df_transformed)

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE parking_summary USING DELTA
# MAGIC AS SELECT * FROM parking_sessions_source WHERE status = 'Completed';
# MAGIC SELECT * FROM parking_summary;

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO parking_sessions_work VALUES
# MAGIC (123, 'Z01', 'Car', 3, 150, 'Active');

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM parking_sessions_work WHERE session_id = 123;

# COMMAND ----------

# MAGIC %sql
# MAGIC UPDATE parking_sessions_work SET status = 'Completed', parking_fee = 280
# MAGIC WHERE session_id = 104;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM parking_sessions_work WHERE session_id = 104;

# COMMAND ----------

# MAGIC %sql
# MAGIC DELETE FROM parking_sessions_work WHERE status = 'Cancelled';

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM parking_sessions_work;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC     i.session_id AS incoming_id, 
# MAGIC     w.session_id AS existing_id,
# MAGIC     CASE WHEN w.session_id IS NOT NULL THEN 'Matches Existing' ELSE 'New Record' END AS match_status
# MAGIC FROM incoming_parking_sessions i
# MAGIC LEFT JOIN parking_sessions_work w 
# MAGIC ON i.session_id = w.session_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC MERGE INTO parking_sessions_work AS target
# MAGIC USING incoming_parking_sessions AS source
# MAGIC ON target.session_id = source.session_id
# MAGIC WHEN MATCHED THEN
# MAGIC UPDATE SET
# MAGIC     zone_id = source.zone_id,
# MAGIC     vehicle_type = source.vehicle_type,
# MAGIC     duration_hours = source.duration_hours,
# MAGIC     parking_fee = source.parking_fee,
# MAGIC     status = source.status
# MAGIC WHEN NOT MATCHED THEN
# MAGIC   INSERT *;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY parking_sessions_work;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM parking_sessions_work VERSION AS OF 3 WHERE session_id = 102;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM parking_sessions_work WHERE session_id = 102;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM parking_sessions_work WHERE session_id = 102;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE VIEW completed_parking_view AS 
# MAGIC SELECT * 
# MAGIC FROM parking_sessions_work 
# MAGIC WHERE status = 'Completed';

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM completed_parking_view;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMPORARY VIEW temp_zone_z01_view AS
# MAGIC SELECT * FROM parking_sessions_work WHERE zone_id = 'Z01';

# COMMAND ----------

# DBTITLE 1,Fix view type for serverless compute
# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMPORARY VIEW global_high_fee_view AS
# MAGIC SELECT * FROM parking_sessions_work WHERE parking_fee > 200;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM temp_zone_z01_view;

# COMMAND ----------

# DBTITLE 1,Fix temp view reference
# MAGIC %sql
# MAGIC SELECT * FROM global_high_fee_view;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   z.zone_name,
# MAGIC   z.city,
# MAGIC   w.vehicle_type,
# MAGIC   w.parking_fee
# MAGIC FROM parking_sessions_work w
# MAGIC INNER JOIN parking_zones z
# MAGIC ON w.zone_id = z.zone_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE DETAIL parking_sessions_work;

# COMMAND ----------

# MAGIC %sql
# MAGIC OPTIMIZE parking_sessions_work;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE DETAIL parking_sessions_work;

# COMMAND ----------

spark.sql("CREATE VOLUME IF NOT EXISTS workspace.default.streaming_checkpoints")
rate_df = spark.readStream \
    .format("rate") \
    .option("rowsPerSecond", 5) \
    .load()
query = rate_df.writeStream \
    .format("console") \
    .outputMode("append") \
    .option("checkpointLocation", "/Volumes/workspace/default/streaming_checkpoints/rate_console") \
    .trigger(availableNow=True) \
    .start()

# COMMAND ----------

from pyspark.sql.functions import col
transformed_stream_df = (streaming_rate_df
                         .withColumn("amount", col("value") * 10)  
                         .filter(col("amount") > 300))
display(transformed_stream_df, outputMode="append", checkpointLocation="/Volumes/workspace/default/streaming_checkpoints/transformed_stream_df")

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REFRESH STREAMING TABLE parking_bronze
# MAGIC COMMENT "Raw real-time ingestion layer for parking session events"
# MAGIC AS SELECT * FROM STREAM(live.parking_sessions_source);

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REFRESH STREAMING TABLE parking_silver
# MAGIC COMMENT "Cleaned streaming records containing only completed sessions"
# MAGIC AS SELECT * 
# MAGIC    FROM STREAM(live.parking_bronze)
# MAGIC    WHERE status = 'Completed';

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REFRESH MATERIALIZED VIEW parking_gold
# MAGIC COMMENT "Aggregated business view for zone-based revenue calculations"
# MAGIC AS SELECT 
# MAGIC     zone_id,
# MAGIC     COUNT(session_id) AS total_completed_sessions,
# MAGIC     SUM(parking_fee) AS total_parking_revenue
# MAGIC FROM live.parking_silver
# MAGIC GROUP BY zone_id;