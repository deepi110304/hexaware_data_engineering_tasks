CREATE OR REFRESH STREAMING TABLE water_bronze_readings
AS
SELECT *
FROM STREAM(workspace.default.water_meter_readings_source);

CREATE OR REFRESH STREAMING TABLE water_silver_readings
AS
SELECT *
FROM STREAM(water_bronze_readings)
WHERE reading_status = 'Valid'
AND flow_lpm > 0
AND consumption_liters > 0;

CREATE OR REFRESH MATERIALIZED VIEW water_gold_zone_summary
AS
SELECT
    zone_id,
    SUM(consumption_liters) AS total_consumption,
    AVG(pressure_bar) AS average_pressure,
    COUNT(*) AS reading_count
FROM water_silver_readings
GROUP BY zone_id;

-- BRONZE: SMART METER READINGS

CREATE OR REFRESH STREAMING TABLE water_readings_bronze
AS
SELECT *
FROM STREAM(workspace.default.water_meter_readings_source);


-- BRONZE: WATER ZONE MASTER

CREATE OR REFRESH MATERIALIZED VIEW water_zones_bronze
AS
SELECT *
FROM workspace.default.water_zones;


-- BRONZE: SERVICE REQUESTS

CREATE OR REFRESH MATERIALIZED VIEW water_service_requests_bronze
AS
SELECT *
FROM workspace.default.water_service_requests;

CREATE OR REFRESH MATERIALIZED VIEW water_readings_silver
AS

WITH ranked_readings AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY reading_id
            ORDER BY reading_time DESC
        ) AS row_num

    FROM water_readings_bronze
)

SELECT
    reading_id,
    meter_id,
    zone_id,
    reading_time,
    flow_lpm,
    pressure_bar,
    chlorine_mg_l,
    consumption_liters,
    reading_status,
    source_system

FROM ranked_readings

WHERE row_num = 1
AND reading_status = 'Valid'
AND zone_id IS NOT NULL
AND flow_lpm > 0
AND consumption_liters > 0;

CREATE OR REFRESH MATERIALIZED VIEW water_quality_silver
AS
SELECT
    *,
    CASE
        WHEN pressure_bar IS NULL THEN 'Missing Pressure'
        WHEN pressure_bar < 2.5 THEN 'Low Pressure'
        ELSE 'Normal Pressure'
    END AS pressure_status,

    CASE
        WHEN chlorine_mg_l IS NULL THEN 'Missing Chlorine Data'
        ELSE 'Chlorine Recorded'
    END AS chlorine_status

FROM water_readings_silver;

CREATE OR REFRESH MATERIALIZED VIEW water_readings_with_zones_silver
AS
SELECT
    r.*,
    z.zone_name,
    z.district,
    z.zone_type,
    z.daily_capacity_liters

FROM water_quality_silver r

LEFT JOIN water_zones_bronze z
ON r.zone_id = z.zone_id;

CREATE OR REFRESH MATERIALIZED VIEW water_zone_summary_gold
AS
SELECT
    zone_id,
    zone_name,
    district,
    zone_type,

    SUM(consumption_liters) AS total_consumption,

    AVG(consumption_liters) AS average_consumption,

    AVG(flow_lpm) AS average_flow,

    AVG(pressure_bar) AS average_pressure,

    AVG(chlorine_mg_l) AS average_chlorine,

    COUNT(*) AS reading_count,

    SUM(
        CASE
            WHEN pressure_bar < 2.5 THEN 1
            ELSE 0
        END
    ) AS low_pressure_count

FROM water_readings_with_zones_silver

GROUP BY
    zone_id,
    zone_name,
    district,
    zone_type;

CREATE OR REFRESH MATERIALIZED VIEW water_district_summary_gold
AS
SELECT
    district,

    SUM(consumption_liters) AS total_consumption,

    AVG(pressure_bar) AS average_pressure,

    AVG(chlorine_mg_l) AS average_chlorine,

    COUNT(*) AS total_readings,

    SUM(
        CASE
            WHEN pressure_bar < 2.5 THEN 1
            ELSE 0
        END
    ) AS low_pressure_count

FROM water_readings_with_zones_silver

GROUP BY district;

CREATE OR REFRESH MATERIALIZED VIEW water_quality_alerts_gold
AS
SELECT
    zone_id,
    zone_name,
    district,
    reading_id,
    pressure_bar,
    chlorine_mg_l,
    pressure_status,
    chlorine_status

FROM water_quality_silver

LEFT JOIN water_zones_bronze
USING (zone_id)

WHERE pressure_bar < 2.5
OR pressure_bar IS NULL
OR chlorine_mg_l IS NULL;

CREATE OR REFRESH MATERIALIZED VIEW gold_service_request_summary
AS
SELECT
    zone_id,

    COUNT(*) AS total_requests,

    SUM(
        CASE
            WHEN priority = 'High' THEN 1
            ELSE 0
        END
    ) AS high_priority_requests,

    SUM(
        CASE
            WHEN priority = 'Medium' THEN 1
            ELSE 0
        END
    ) AS medium_priority_requests,

    SUM(
        CASE
            WHEN priority = 'Low' THEN 1
            ELSE 0
        END
    ) AS low_priority_requests

FROM water_service_requests_bronze

GROUP BY zone_id;