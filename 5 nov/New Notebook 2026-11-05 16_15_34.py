# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE cafe_orders_demo (
# MAGIC     order_id INT,
# MAGIC     customer_name STRING,
# MAGIC     city STRING,
# MAGIC     amount INT,
# MAGIC     order_status STRING
# MAGIC )
# MAGIC USING DELTA;

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO cafe_orders_demo VALUES
# MAGIC (101, 'Ayaan', 'Hyderabad', 450, 'Completed'),
# MAGIC (102, 'Tara', 'Mumbai', 700, 'Pending'),
# MAGIC (103, 'Ishaan', 'Pune', 300, 'Completed'),
# MAGIC (104, 'Sara', 'Hyderabad', 900, 'Completed'),
# MAGIC (105, 'Kabir', 'Delhi', 250, 'Cancelled'),
# MAGIC (106, 'Zoya', 'Mumbai', 600, 'Pending'),
# MAGIC (107, 'Rehan', 'Pune', 800, 'Completed'),
# MAGIC (108, 'Mira', 'Delhi', 550, 'Completed');

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE EXTENDED cafe_orders_demo;

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW CATALOGS

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG databricks_deepikaa;

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW SCHEMAS;

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW SCHEMAS;

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW TABLES;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT current_catalog(), current_schema();