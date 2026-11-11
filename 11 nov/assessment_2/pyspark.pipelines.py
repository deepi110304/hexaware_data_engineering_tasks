from pyspark import pipelines as dp
from pyspark.sql.functions import col, sum, avg, count
# Bronze
@dp.table(name="bronze_water_readings_py")
def bronze_water_readings_py():

    return spark.readStream.table(
        "workspace.default.water_meter_readings_source"
    )
# Silver
@dp.table(name="silver_water_readings_py")
def silver_water_readings_py():

    readings_df = spark.readStream.table(
        "bronze_water_readings_py"
    )

    return readings_df.filter(
        (col("reading_status") == "Valid") &
        (col("flow_lpm") > 0) &
        (col("consumption_liters") > 0)
    )


# Gold
@dp.materialized_view(name="gold_water_summary_py")
def gold_water_summary_py():

    readings_df = spark.read.table(
        "silver_water_readings_py"
    )

    return readings_df.groupBy(
        "zone_id"
    ).agg(
        sum("consumption_liters").alias("total_consumption"),
        avg("pressure_bar").alias("average_pressure"),
        avg("chlorine_mg_l").alias("average_chlorine"),
        count("*").alias("reading_count")
    )