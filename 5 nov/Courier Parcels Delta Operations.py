# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE courier_parcels_delta (
# MAGIC     parcel_id INT,
# MAGIC     customer_name STRING,
# MAGIC     destination_city STRING,
# MAGIC     service_type STRING,
# MAGIC     weight_kg DOUBLE,
# MAGIC     shipping_fee INT,
# MAGIC     delivery_status STRING
# MAGIC )
# MAGIC USING DELTA;

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO courier_parcels_delta VALUES
# MAGIC (101, 'Arjun', 'Hyderabad', 'Express', 2.5, 500, 'Delivered'),
# MAGIC (102, 'Meera', 'Mumbai', 'Standard', 4.0, 350, 'In Transit'),
# MAGIC (103, 'Karan', 'Delhi', 'Express', 1.5, 450, 'Pending'),
# MAGIC (104, 'Sneha', 'Pune', 'Standard', 3.0, 300, 'Delivered'),
# MAGIC (105, 'Rohit', 'Chennai', 'Express', 5.0, 800, 'In Transit'),
# MAGIC (106, 'Divya', 'Hyderabad', 'Standard', 2.0, 250, 'Cancelled'),
# MAGIC (107, 'Nikhil', 'Bengaluru', 'Express', 6.0, 950, 'Delivered'),
# MAGIC (108, 'Pooja', 'Mumbai', 'Standard', 1.0, 150, 'Pending'),
# MAGIC (109, 'Vikram', 'Delhi', 'Express', 3.5, 650, 'In Transit'),
# MAGIC (110, 'Anjali', 'Pune', 'Standard', 4.5, 400, 'Cancelled'),
# MAGIC (111, 'Farhan', 'Chennai', 'Express', 2.0, 550, 'Delivered'),
# MAGIC (112, 'Kavya', 'Hyderabad', 'Standard', 5.5, 600, 'Pending'),
# MAGIC (113, 'Manoj', 'Bengaluru', 'Express', 1.5, 400, 'In Transit'),
# MAGIC (114, 'Riya', 'Delhi', 'Standard', 3.0, 300, 'Delivered'),
# MAGIC (115, 'Tarun', 'Mumbai', 'Express', 4.0, 700, 'Pending');

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM courier_parcels_delta;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE courier_parcels_copy USING DELTA AS SELECT * FROM courier_parcels_delta;

# COMMAND ----------

# Run this in a Python cell
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType

schema = StructType([
    StructField("parcel_id", IntegerType(), True),
    StructField("customer_name", StringType(), True),
    StructField("destination_city", StringType(), True),
    StructField("service_type", StringType(), True),
    StructField("weight_kg", DoubleType(), True),
    StructField("shipping_fee", IntegerType(), True),
    StructField("delivery_status", StringType(), True)
])

new_data = [
    (119, 'Amit', 'Kochi', 'Express', 1.8, 400, 'Pending'),
    (120, 'Sonia', 'Goa', 'Standard', 3.2, 280, 'In Transit'),
    (121, 'Vijay', 'Patna', 'Express', 2.2, 500, 'Delivered')
]

df = spark.createDataFrame(new_data, schema)
df.write.format("delta").mode("overwrite").saveAsTable("courier_parcels_pyspark")


# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW TABLES;
# MAGIC DESCRIBE EXTENDED courier_parcels_delta;
# MAGIC DESCRIBE EXTENDED courier_parcels_copy;
# MAGIC DESCRIBE EXTENDED courier_parcels_pyspark;

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO courier_parcels_delta VALUES
# MAGIC (116, 'Sameer', 'Jaipur', 'Express', 2.5, 550, 'Pending');

# COMMAND ----------

# MAGIC %sql
# MAGIC UPDATE courier_parcels_delta 
# MAGIC SET delivery_status = 'Delivered' 
# MAGIC WHERE parcel_id = 103;

# COMMAND ----------

# MAGIC %sql
# MAGIC UPDATE courier_parcels_delta 
# MAGIC SET shipping_fee = shipping_fee + 100 
# MAGIC WHERE service_type = 'Express';

# COMMAND ----------

# MAGIC %sql
# MAGIC UPDATE courier_parcels_delta 
# MAGIC SET destination_city = 'Hyderabad' 
# MAGIC WHERE parcel_id = 108;

# COMMAND ----------

# MAGIC %sql
# MAGIC DELETE FROM courier_parcels_delta 
# MAGIC WHERE delivery_status = 'Cancelled';

# COMMAND ----------

# DBTITLE 1,Create incoming_parcels table
# MAGIC %sql
# MAGIC -- Incoming parcel feed: updates to existing parcels (102, 105, 108) and new parcels (122-124)
# MAGIC CREATE OR REPLACE TABLE incoming_parcels
# MAGIC USING DELTA
# MAGIC AS SELECT
# MAGIC     CAST(parcel_id AS INT) AS parcel_id,
# MAGIC     CAST(customer_name AS STRING) AS customer_name,
# MAGIC     CAST(destination_city AS STRING) AS destination_city,
# MAGIC     CAST(service_type AS STRING) AS service_type,
# MAGIC     CAST(weight_kg AS DOUBLE) AS weight_kg,
# MAGIC     CAST(shipping_fee AS INT) AS shipping_fee,
# MAGIC     CAST(delivery_status AS STRING) AS delivery_status
# MAGIC FROM VALUES
# MAGIC (102, 'Meera', 'Mumbai', 'Standard', 4.0, 350, 'Delivered'),
# MAGIC (105, 'Rohit', 'Chennai', 'Express', 5.0, 900, 'Delivered'),
# MAGIC (108, 'Pooja', 'Hyderabad', 'Standard', 1.0, 150, 'In Transit'),
# MAGIC (122, 'Lakshmi', 'Kolkata', 'Express', 2.8, 600, 'Pending'),
# MAGIC (123, 'Harish', 'Ahmedabad', 'Standard', 3.6, 320, 'In Transit'),
# MAGIC (124, 'Neha', 'Lucknow', 'Express', 1.2, 450, 'Pending')
# MAGIC AS t(parcel_id, customer_name, destination_city, service_type, weight_kg, shipping_fee, delivery_status);

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM incoming_parcels;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT i.parcel_id, i.customer_name 
# MAGIC FROM incoming_parcels i 
# MAGIC INNER JOIN courier_parcels_delta t 
# MAGIC ON i.parcel_id = t.parcel_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT i.parcel_id, i.customer_name 
# MAGIC FROM incoming_parcels i 
# MAGIC LEFT JOIN courier_parcels_delta t 
# MAGIC ON i.parcel_id = t.parcel_id 
# MAGIC WHERE t.parcel_id IS NULL;

# COMMAND ----------

# MAGIC %sql
# MAGIC MERGE INTO courier_parcels_delta AS target
# MAGIC USING incoming_parcels AS source
# MAGIC ON target.parcel_id = source.parcel_id
# MAGIC WHEN MATCHED THEN
# MAGIC   UPDATE SET
# MAGIC     target.customer_name = source.customer_name,
# MAGIC     target.destination_city = source.destination_city,
# MAGIC     target.service_type = source.service_type,
# MAGIC     target.weight_kg = source.weight_kg,
# MAGIC     target.shipping_fee = source.shipping_fee,
# MAGIC     target.delivery_status = source.delivery_status
# MAGIC WHEN NOT MATCHED THEN
# MAGIC   INSERT (parcel_id, customer_name, destination_city, service_type, weight_kg, shipping_fee, delivery_status)
# MAGIC   VALUES (source.parcel_id, source.customer_name, source.destination_city, source.service_type, source.weight_kg, source.shipping_fee, source.delivery_status);
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM courier_parcels_delta WHERE parcel_id IN (102, 105);

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM courier_parcels_delta WHERE parcel_id IN (117, 118);

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE DETAIL courier_parcels_delta;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY courier_parcels_delta;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM courier_parcels_delta VERSION AS OF 1;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 'Previous' AS state, * FROM courier_parcels_delta VERSION AS OF 4 WHERE parcel_id = 102
# MAGIC UNION ALL
# MAGIC SELECT 'Current' AS state, * FROM courier_parcels_delta WHERE parcel_id = 102;

# COMMAND ----------

# MAGIC %sql
# MAGIC OPTIMIZE courier_parcels_delta;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE DETAIL courier_parcels_delta;

# COMMAND ----------

# MAGIC %sql
# MAGIC OPTIMIZE courier_parcels_delta ZORDER BY (destination_city);

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY courier_parcels_delta;