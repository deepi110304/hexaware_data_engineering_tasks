import csv
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator


def load_batches():
    with open("/opt/airflow/dags/factory_batches.csv", newline="") as file:
        rows = list(csv.DictReader(file))
    print("Batches loaded:", len(rows))
    return rows


def check_quality(ti):
    batches = ti.xcom_pull(task_ids="load_batches")
    review_batches = []

    for batch in batches:
        units = int(batch["units_produced"])
        defective = int(batch["defective_units"])
        defect_percentage = (defective / units) * 100

        if defect_percentage > 5:
            review_batches.append(batch["batch_id"])

    print("Batches requiring quality review:", review_batches)
    return review_batches


def calculate_value(ti):
    batches = ti.xcom_pull(task_ids="load_batches")
    total_value = 0

    for batch in batches:
        units = int(batch["units_produced"])
        value = int(batch["value_per_unit"])
        total_value += units * value

    print("Total production value:", total_value)
    return total_value


def generate_report(ti):
    batches = ti.xcom_pull(task_ids="load_batches")
    review_batches = ti.xcom_pull(task_ids="check_quality")
    total_value = ti.xcom_pull(task_ids="calculate_value")

    print("========== MANUFACTURING BATCH QUALITY REPORT ==========")
    print("Total number of batches:", len(batches))
    print("Batches requiring quality review:", review_batches)
    print("Total production value:", total_value)
    print("========================================================")


with DAG(
    dag_id="factory_quality_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False
) as dag:

    load_task = PythonOperator(
        task_id="load_batches",
        python_callable=load_batches
    )

    quality_task = PythonOperator(
        task_id="check_quality",
        python_callable=check_quality
    )

    value_task = PythonOperator(
        task_id="calculate_value",
        python_callable=calculate_value
    )

    report_task = PythonOperator(
        task_id="generate_report",
        python_callable=generate_report
    )

    load_task >> [quality_task, value_task] >> report_task
