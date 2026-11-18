# Databricks notebook source
sales_path = "/Workspace/Users/deepikavu11@gmail.com/cleaned_sales.csv"
product_path = "/Workspace/Users/deepikavu11@gmail.com/product_sales_summary.csv"

# COMMAND ----------

sales_df = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load(sales_path)
display(sales_df)

# COMMAND ----------

print("Total sales records:", sales_df.count())
sales_df.printSchema()

# COMMAND ----------

product_df = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load(product_path)
display(product_df)

# COMMAND ----------

from pyspark.sql.functions import (
    col,
    when,
    round,
    sum,
    avg
)

# COMMAND ----------

sales_df = sales_df.withColumn(
    "net_revenue",
    col("net_revenue").cast("double")
)
sales_df = sales_df.withColumn(
    "total_cost",
    col("total_cost").cast("double")
)
sales_df = sales_df.withColumn(
    "profit",
    col("net_revenue") - col("total_cost")
)
sales_df = sales_df.withColumn(
    "profit_margin_percent",
    when(
        col("net_revenue") > 0,
        round(
            col("profit") / col("net_revenue") * 100,
            2
        )
    ).otherwise(0)
)
display(sales_df)

# COMMAND ----------

product_dimension = product_df.select(
    "product_id",
    "product_name",
    "category"
).dropDuplicates(["product_id"])

# COMMAND ----------

joined_df = sales_df.alias("s").join(
    product_dimension.alias("p"),
    col("s.product_id") == col("p.product_id"),
    "inner"
).select(
    col("s.sale_id"),
    col("s.sale_date"),
    col("s.product_id"),
    col("p.product_name"),
    col("p.category"),
    col("s.store_id"),
    col("s.store_name"),
    col("s.region"),
    col("s.quantity"),
    col("s.unit_price"),
    col("s.net_revenue"),
    col("s.total_cost"),
    col("s.profit"),
    col("s.profit_margin_percent")
)
display(joined_df)

# COMMAND ----------

print("Sales records:", sales_df.count())
print("Product records:", product_dimension.count())
print("Joined records:", joined_df.count())

# COMMAND ----------

category_metrics = joined_df.groupBy("category").agg(
    sum("net_revenue").alias("total_revenue"),
    sum("total_cost").alias("total_cost"),
    sum("profit").alias("total_profit"),
    sum("quantity").alias("total_quantity"),
    avg("profit_margin_percent").alias("average_margin")
)

# COMMAND ----------

category_metrics = category_metrics.withColumn(
    "profit_margin_percent",
    round(
        col("total_profit") / col("total_revenue") * 100,
        2
    )
)
display(category_metrics)

# COMMAND ----------

# DBTITLE 1,Write category metrics table
category_metrics.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("workspace.retail_etl.retail_category_metrics")
display(spark.table("workspace.retail_etl.retail_category_metrics"))

# COMMAND ----------

category_metrics.coalesce(1).write \
    .format("csv") \
    .option("header", "true") \
    .mode("overwrite") \
    .save("/Volumes/workspace/retail_etl/retail_files/retail_category_metrics")

# COMMAND ----------

joined_df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("workspace.retail_etl.retail_sales_enriched_week4")

# COMMAND ----------

# DBTITLE 1,Top products by sales
# MAGIC %sql
# MAGIC SELECT
# MAGIC     product_id,
# MAGIC     product_name,
# MAGIC     category,
# MAGIC     SUM(quantity) AS total_quantity_sold,
# MAGIC     SUM(net_revenue) AS total_revenue,
# MAGIC     SUM(profit) AS total_profit
# MAGIC FROM workspace.retail_etl.retail_sales_enriched_week4
# MAGIC GROUP BY
# MAGIC     product_id,
# MAGIC     product_name,
# MAGIC     category
# MAGIC ORDER BY
# MAGIC     total_quantity_sold DESC,
# MAGIC     total_revenue DESC
# MAGIC LIMIT 3;

# COMMAND ----------

display(spark.sql("SHOW TABLES IN workspace.retail_etl"))

df = spark.table("workspace.retail_etl.retail_sales_enriched_week4")

# 1. Save as a single CSV file
df.coalesce(1).write.mode("overwrite").option("header", "true").csv("/Volumes/workspace/retail_etl/retail_files/week4_csv")

# 2. Save in Delta format
df.write.format("delta").mode("overwrite").save("/Volumes/workspace/retail_etl/retail_files/week4_delta")
