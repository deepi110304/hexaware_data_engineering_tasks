# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE retail_products_sql (
# MAGIC     product_id INT,
# MAGIC     product_name STRING,
# MAGIC     price INT
# MAGIC )
# MAGIC USING DELTA;

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO retail_products_sql VALUES 
# MAGIC (1, 'Laptop', 50000),
# MAGIC (2, 'Mouse', 800),
# MAGIC (3, 'Keyboard', 1500);

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM retail_products_sql;

# COMMAND ----------

data = [
    (4, "Monitor", 12000),
    (5, "Printer", 18000),
    (6, "Webcam", 2500)
]
 
df = spark.createDataFrame(
    data,
    ["product_id", "product_name", "price"]
)
 
df.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("retail_products_pyspark")
 
display(spark.table("retail_products_pyspark"))

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE retail_products_ctas
# MAGIC USING DELTA
# MAGIC AS
# MAGIC SELECT *
# MAGIC FROM VALUES
# MAGIC     (7, 'Tablet', 25000),
# MAGIC     (8, 'Speaker', 5000),
# MAGIC     (9, 'Router', 3500)
# MAGIC AS products(product_id, product_name, price);

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM retail_products_ctas;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMP VIEW product_updates AS
# MAGIC SELECT *
# MAGIC FROM VALUES
# MAGIC     (2, 'Wireless Mouse', 950),
# MAGIC     (10, 'USB Hub', 1200)
# MAGIC AS updates(product_id, product_name, price);

# COMMAND ----------

# MAGIC %sql
# MAGIC MERGE INTO retail_products_sql AS target
# MAGIC USING product_updates AS source
# MAGIC ON target.product_id = source.product_id
# MAGIC
# MAGIC WHEN MATCHED THEN
# MAGIC     UPDATE SET
# MAGIC         target.product_name = source.product_name,
# MAGIC         target.price = source.price
# MAGIC
# MAGIC WHEN NOT MATCHED THEN
# MAGIC     INSERT (product_id, product_name, price)
# MAGIC     VALUES (source.product_id, source.product_name, source.price);

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM retail_products_sql ORDER BY product_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE DETAIL retail_products_sql;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY retail_products_sql;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT* FROM retail_products_sql VERSION AS OF 1;

# COMMAND ----------

# MAGIC %sql
# MAGIC OPTIMIZE retail_products_sql;

# COMMAND ----------

# MAGIC %sql
# MAGIC OPTIMIZE retail_products_sql ZORDER BY (product_id);