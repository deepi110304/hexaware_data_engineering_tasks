# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE event_registrations_source (
# MAGIC     registration_id INT,
# MAGIC     event_id STRING,
# MAGIC     attendee_name STRING,
# MAGIC     registration_date STRING,
# MAGIC     ticket_type STRING,
# MAGIC     tickets INT,
# MAGIC     unit_price INT,
# MAGIC     status STRING,
# MAGIC     channel STRING
# MAGIC )
# MAGIC USING DELTA;

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO event_registrations_source VALUES
# MAGIC (2001,'E01','Aarav','2026-10-01','Standard',2,500,'Confirmed','Web'),
# MAGIC (2002,'E02','Arnav','2026-10-02','Premium',1,1200,'Confirmed','App'),
# MAGIC (2003,'E03','Bhavna','2026-10-03','Standard',3,800,'Pending','Counter'),
# MAGIC (2004,'E04','Charan','2026-10-04','Standard',2,650,'Confirmed','Partner'),
# MAGIC (2005,'E05','Diya','2026-10-05','VIP',1,1500,'Cancelled','Web'),
# MAGIC (2006,'E06','Eshan','2026-10-06','Standard',4,400,'Confirmed','App'),
# MAGIC (2007,'E01','Fiza','2026-10-07','Premium',1,1000,'Confirmed','App'),
# MAGIC (2008,'E02','Farah','2026-10-08','Premium',2,1200,'Pending','Web'),
# MAGIC (2009,'E03','Gauri','2026-10-09','Standard',1,800,'Confirmed','Counter'),
# MAGIC (2010,'E04','Harini','2026-10-10','Standard',3,650,'Confirmed','Web'),
# MAGIC (2011,'E05','Irfan','2026-10-11','VIP',2,1500,'Confirmed','Partner'),
# MAGIC (2012,'E06','Jiya','2026-10-12','Standard',1,400,'Cancelled','App'),
# MAGIC (2013,'E01','Kabir','2026-10-13','Standard',4,500,'Confirmed','Web'),
# MAGIC (2014,'E02','Lakshmi','2026-10-14','VIP',1,1800,'Confirmed','Counter'),
# MAGIC (2015,'E03','Mohan','2026-10-15','Standard',2,800,'Confirmed','Partner'),
# MAGIC (2016,'E04','Nisha','2026-10-16','Standard',1,650,'Pending','Web'),
# MAGIC (2017,'E05','Omkar','2026-10-17','VIP',3,1500,'Confirmed','App'),
# MAGIC (2018,'E06','Pari','2026-10-18','Standard',2,400,'Confirmed','Web'),
# MAGIC (2019,'E01','Qadir','2026-10-19','Standard',2,500,'Cancelled','Counter'),
# MAGIC (2020,'E02','Rohan','2026-10-20','Premium',3,1200,'Confirmed','Partner'),
# MAGIC (2021,'E03','Sana','2026-10-21','Premium',1,1300,'Confirmed','App'),
# MAGIC (2022,'E04','Tanvi','2026-10-22','Standard',2,650,'Confirmed',NULL),
# MAGIC (2023,'E05','Uday','2026-10-23','VIP',1,1500,'Pending','Web'),
# MAGIC (2024,'E06','Imran','2026-10-24','Standard',3,400,'Confirmed','App'),
# MAGIC (2025,'E01','Varsha','2026-10-25','Standard',1,500,'Confirmed','Web'),
# MAGIC (2026,'E02','Wasim','2026-10-26','Premium',2,1200,'Confirmed',NULL),
# MAGIC (2027,'E03','Yash','2026-10-27','Standard',0,800,'Pending','Counter'),
# MAGIC (2028,'E04','Zara','2026-10-28','Standard',2,0,'Confirmed','Web'),
# MAGIC (2029,'E05','Adil','2026-10-29','VIP',2,1500,'Confirmed','App'),
# MAGIC (2030,'E06','Bina','2026-10-30','Standard',1,400,'Pending','Counter'),
# MAGIC (2031,'E99','Chetan','2026-10-31','Standard',2,700,'Confirmed','Web'),
# MAGIC (2032,'E01','Danish','2026-11-01','Standard',3,500,'Confirmed','Partner');

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE event_master (
# MAGIC     event_id STRING,
# MAGIC     event_name STRING,
# MAGIC     city STRING,
# MAGIC     category STRING,
# MAGIC     capacity INT
# MAGIC )
# MAGIC USING DELTA;

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO event_master VALUES
# MAGIC ('E01','Design Summit','Bengaluru','Technology',300),
# MAGIC ('E02','Food Expo','Hyderabad','Culinary',250),
# MAGIC ('E03','Art Fair','Pune','Culture',180),
# MAGIC ('E04','Startup Meetup','Mumbai','Business',220),
# MAGIC ('E05','Music Showcase','Chennai','Entertainment',400),
# MAGIC ('E06','Book Festival','Delhi','Literature',150),
# MAGIC ('E07','Photography Walk','Jaipur','Culture',90);

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE event_registrations_work
# MAGIC USING DELTA
# MAGIC AS
# MAGIC SELECT * FROM event_registrations_source;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMP VIEW incoming_registrations AS
# MAGIC SELECT *
# MAGIC FROM VALUES
# MAGIC (2002,'E02','Arnav','2026-10-02','Premium',1,1400,'Confirmed','App'),
# MAGIC (2008,'E02','Farah','2026-10-08','Premium',2,1200,'Confirmed','Web'),
# MAGIC (2024,'E06','Imran','2026-10-24','Standard',3,450,'Confirmed','App'),
# MAGIC (2033,'E07','Naina','2026-11-05','Standard',2,600,'Confirmed','Web'),
# MAGIC (2034,'E03','Omar','2026-11-05','Premium',1,900,'Pending','Partner'),
# MAGIC (2035,'E05','Leena','2026-11-06','VIP',2,1600,'Confirmed','App')
# MAGIC AS t(
# MAGIC registration_id,event_id,attendee_name,
# MAGIC registration_date,ticket_type,tickets,
# MAGIC unit_price,status,channel
# MAGIC );

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM event_registrations_source;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT registration_id, attendee_name, event_id, unit_price 
# MAGIC FROM event_registrations_source;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM event_registrations_source WHERE status = 'Confirmed';

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM event_registrations_source WHERE unit_price > 1000;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM event_registrations_source WHERE ticket_type IN('Premium','VIP');

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM event_registrations_source WHERE unit_price BETWEEN 500 AND 1200
# MAGIC ORDER BY unit_price DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT DISTINCT channel FROM event_registrations_source;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM event_registrations_source WHERE attendee_name LIKE 'A%' OR attendee_name LIKE 'a%'

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT event_id, SUM(tickets) AS total_tickets
# MAGIC FROM event_registrations_source
# MAGIC GROUP BY event_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT event_id, SUM(tickets * unit_price) AS total_revenue
# MAGIC FROM event_registrations_source
# MAGIC WHERE status = 'Confirmed' AND tickets > 0 AND unit_price > 0 
# MAGIC GROUP BY event_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC    r.attendee_name,
# MAGIC    m.event_name,
# MAGIC    m.city,
# MAGIC    r.ticket_type,
# MAGIC    r.status
# MAGIC FROM event_registrations_source r
# MAGIC INNER JOIN event_master m 
# MAGIC ON r.event_id = m.event_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT r.* 
# MAGIC FROM event_registrations_source r 
# MAGIC LEFT JOIN event_master m ON r.event_id = m.event_id 
# MAGIC WHERE m.event_id IS NULL;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT m.* 
# MAGIC FROM event_master m 
# MAGIC LEFT JOIN event_registrations_source r ON m.event_id = r.event_id 
# MAGIC WHERE r.event_id IS NULL;

# COMMAND ----------

df_registrations = spark.read.table("event_registrations_source")
df_master = spark.read.table("event_master")
print("--- Registrations Schema ---")
df_registrations.printSchema()
print("--- Event Master Schema ---")
df_master.printSchema()

# COMMAND ----------

df_selected = df_registrations.select("registration_id", "attendee_name", "tickets", "unit_price")
df_selected.show()

# COMMAND ----------

df_filtered = df_registrations.filter((df_registrations.status == "Confirmed") & (df_registrations.tickets > 2))
df_filtered.show() 

# COMMAND ----------

from pyspark.sql.functions import col
df_with_total = df_registrations.withColumn("total_amount", col("tickets") * col("unit_price"))
df_with_total.show()

# COMMAND ----------

from pyspark.sql.functions import when
df_category = df_with_total.withColumn(
    "booking_category",
     when(col("total_amount") >= 2000, "High").otherwise("Regular")
)
df_category.show()

# COMMAND ----------

from pyspark.sql.functions import col, sum
df_joined_revenue = (df_registrations 
    .join(df_master, "event_id", "inner") 
    .filter(col("status") == "Confirmed") 
    .withColumn("revenue", col("tickets") * col("unit_price")) 
    .groupBy("city") 
    .agg(sum("revenue").alias("total_confirmed_revenue")))
df_joined_revenue.show()


# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE confirmed_event_registrations 
# MAGIC USING DELTA 
# MAGIC AS 
# MAGIC SELECT * FROM event_registrations_source 
# MAGIC WHERE status = 'Confirmed';

# COMMAND ----------

df_registrations.write.format("delta").mode("overwrite").saveAsTable("event_registrations_pyspark")

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO event_registrations_work VALUES 
# MAGIC (2036, 'E01', 'Amit', '2026-11-06', 'Standard', 1, 2500, 'Confirmed', 'Web'),
# MAGIC (2037, 'E02', 'Neha', '2026-11-06', 'VIP', 1, 1500, 'Pending', 'App');

# COMMAND ----------

# MAGIC %sql
# MAGIC UPDATE event_registrations_work 
# MAGIC SET status = 'Confirmed' 
# MAGIC WHERE registration_id = 2003;

# COMMAND ----------

# MAGIC %sql
# MAGIC UPDATE event_registrations_work 
# MAGIC SET unit_price = unit_price + 200 
# MAGIC WHERE ticket_type = 'VIP';

# COMMAND ----------

# MAGIC %sql
# MAGIC DELETE FROM event_registrations_work 
# MAGIC WHERE status = 'Cancelled';

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) FROM event_registrations_work WHERE status = 'Cancelled';

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM event_registrations_work;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT i.registration_id, 'Existing/Update' AS record_type 
# MAGIC FROM incoming_registrations i
# MAGIC INNER JOIN event_registrations_work w ON i.registration_id = w.registration_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT i.registration_id, 'New/Insert' AS record_type 
# MAGIC FROM incoming_registrations i
# MAGIC LEFT JOIN event_registrations_work w ON i.registration_id = w.registration_id
# MAGIC WHERE w.registration_id IS NULL;

# COMMAND ----------

# DBTITLE 1,Fix cell language and MERGE SET syntax
# MAGIC %sql
# MAGIC MERGE INTO event_registrations_work AS target
# MAGIC USING incoming_registrations AS source
# MAGIC ON target.registration_id = source.registration_id
# MAGIC WHEN MATCHED THEN
# MAGIC   UPDATE SET 
# MAGIC     event_id = source.event_id,
# MAGIC     attendee_name = source.attendee_name,
# MAGIC     registration_date = source.registration_date,
# MAGIC     ticket_type = source.ticket_type,
# MAGIC     tickets = source.tickets,
# MAGIC     unit_price = source.unit_price,
# MAGIC     status = source.status,
# MAGIC     channel = source.channel
# MAGIC WHEN NOT MATCHED THEN
# MAGIC   INSERT (registration_id, event_id, attendee_name, registration_date, ticket_type, tickets, unit_price, status, channel)
# MAGIC   VALUES (source.registration_id, source.event_id, source.attendee_name, source.registration_date, source.ticket_type, source.tickets, source.unit_price, source.status, source.channel);

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM event_registrations_work 
# MAGIC WHERE registration_id IN(2002, 2008, 2024);

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM event_registrations_work 
# MAGIC WHERE registration_id IN (2033, 2034, 2035);

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE DETAIL event_registrations_work;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY event_registrations_work;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM event_registrations_work VERSION AS OF 3 WHERE registration_id = 2002;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 'Historical' AS version_type, * FROM event_registrations_work VERSION AS OF 3 WHERE registration_id = 2002
# MAGIC UNION ALL
# MAGIC SELECT 'Current' AS version_type, * FROM event_registrations_work WHERE registration_id = 2002;

# COMMAND ----------

35. 
• Parquet Files: These are row-oriented, compressed columnar storage files that hold the actual data records of the table. They enable fast read queries by pruning unneeded columns and using statistics.
• _delta_log Directory: This folder sits at the root of the Delta table and contains the central transaction log. It holds JSON commit files like 000000.json, 000001.json, etc. and checkpoint Parquet files. It tracks structural metadata, schema constraints, and tells Spark exactly which Parquet data files are currently valid.

# COMMAND ----------

36. VACUUM Purpose: It cleans up historical Parquet data files that are no longer referenced by the current state of the Delta log and fall outside the retention threshold window.

# COMMAND ----------

# MAGIC %sql
# MAGIC VACUUM event_registrations_work DRY RUN;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE EXTENDED event_registrations_source;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE VIEW event_revenue_view AS 
# MAGIC SELECT 
# MAGIC     m.event_name, 
# MAGIC     m.city, 
# MAGIC     SUM(r.tickets * r.unit_price) AS total_confirmed_revenue
# MAGIC FROM event_registrations_source r
# MAGIC INNER JOIN event_master m ON r.event_id = m.event_id
# MAGIC WHERE r.status = 'Confirmed'
# MAGIC GROUP BY m.event_name, m.city;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMPORARY VIEW pending_registrations_view AS 
# MAGIC SELECT * FROM event_registrations_source 
# MAGIC WHERE status = 'Pending';

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMP VIEW vip_registrations_view AS 
# MAGIC SELECT * FROM event_registrations_source 
# MAGIC WHERE ticket_type = 'VIP';

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM event_revenue_view;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM pending_registrations_view;

# COMMAND ----------

# DBTITLE 1,Fix temp view reference
# MAGIC %sql
# MAGIC SELECT * FROM vip_registrations_view;

# COMMAND ----------

# MAGIC %sql
# MAGIC OPTIMIZE event_registrations_work;

# COMMAND ----------

# MAGIC %sql
# MAGIC OPTIMIZE event_registrations_work ZORDER BY (event_id);

# COMMAND ----------

# DBTITLE 1,Fix catalog name in paths
parquet_path = "/Volumes/workspace/default/my_volume/event_parquet_data"
delta_table_name = "workspace.default.converted_event_delta"
df_master.write.format("parquet").mode("overwrite").save(parquet_path)
spark.sql(f"CONVERT TO DELTA parquet.`{parquet_path}`")
spark.read.format("delta").load(parquet_path).write.format("delta").mode("overwrite").saveAsTable(delta_table_name)

# COMMAND ----------

df_stream_source = spark.readStream \
    .format("rate") \
    .option("rowsPerSecond", 5) \
    .load()

# COMMAND ----------

# DBTITLE 1,Add explicit streaming checkpoint and output mode
display(df_stream_source, outputMode="append", checkpointLocation="/Volumes/workspace/default/streaming_checkpoints/df_stream_source")

# COMMAND ----------

from pyspark.sql.functions import concat, lit, col
df_stream_transformed = df_stream_source \
    .withColumn("transaction_id", concat(lit("TXN-"), col("value"))) \
    .withColumn("transaction_amount", col("value") * 10)

# COMMAND ----------

df_stream_filtered = df_stream_transformed.filter(col("transaction_amount") > 500)

# COMMAND ----------

# DBTITLE 1,Use bounded trigger with explicit checkpoint
from pyspark.sql.functions import expr
df_stream_aggregated = df_stream_filtered \
    .withColumn("transaction_category", when(col("transaction_amount") >= 2000, "Tier-1").otherwise("Tier-2")) \
    .groupBy("transaction_category") \
    .count()
query_stream = df_stream_aggregated.writeStream \
    .format("memory") \
    .queryName("streaming_metrics_summary") \
    .outputMode("complete") \
    .option("checkpointLocation", "/Volumes/workspace/default/streaming_checkpoints/streaming_metrics_summary") \
    .trigger(availableNow=True) \
    .start()
import time
time.sleep(10)
spark.sql("SELECT * FROM streaming_metrics_summary").show()
query_stream.stop()