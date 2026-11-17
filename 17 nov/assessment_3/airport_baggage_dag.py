import csv
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
# TASK 1: Load baggage records from CSV
def load_baggage():
    with open(
        '/opt/airflow/dags/airport_baggage.csv',
        newline=''
    ) as file:
        records = list(csv.DictReader(file))
    print('Baggage records loaded:', len(records))
    return records
# TASK 2: Identify bags requiring manual review
def identify_review_bags(**kwargs):
    ti = kwargs['ti']
    records = ti.xcom_pull(task_ids='load_baggage')
    review_bags = []
    for bag in records:
        weight = int(bag['weight_kg'])
        if bag['screening_status'] == 'Review' or weight > 23:
            review_bags.append(bag['bag_id'])
    print('Bags requiring manual review:', review_bags)
    return review_bags
# TASK 3: Calculate total baggage weight
def calculate_total_weight(**kwargs):
    ti = kwargs['ti']
    records = ti.xcom_pull(task_ids='load_baggage')
    total_weight = sum(
        int(bag['weight_kg']) for bag in records
    )
    print('Total baggage weight:', total_weight, 'kg')
    return total_weight
# TASK 4: Generate final report
def generate_report(**kwargs):
    ti = kwargs['ti']
    records = ti.xcom_pull(task_ids='load_baggage')
    review_bags = ti.xcom_pull(
        task_ids='identify_review_bags'
    )
    total_weight = ti.xcom_pull(
        task_ids='calculate_total_weight'
    )
    print('========== AIRPORT BAGGAGE SCREENING REPORT ==========')
    print('Total number of baggage records:', len(records))
    print('Number of bags requiring review:', len(review_bags))
    print('Bag IDs requiring review:', review_bags)
    print('Total baggage weight:', total_weight, 'kg')
    print('======================================================')
# DEFINE DAG
with DAG(
    dag_id='airport_baggage_pipeline',
    start_date=datetime(2026, 11, 17),
    schedule=None,
    catchup=False,
    tags=['Airport', 'Baggage', 'Assessment']
) as dag:
    load_task = PythonOperator(
        task_id='load_baggage',
        python_callable=load_baggage
    )
    review_task = PythonOperator(
        task_id='identify_review_bags',
        python_callable=identify_review_bags
    )
    weight_task = PythonOperator(
        task_id='calculate_total_weight',
        python_callable=calculate_total_weight
    )
    report_task = PythonOperator(
        task_id='generate_report',
        python_callable=generate_report
    )
    # Parallel task dependencies
    load_task >> [review_task, weight_task]
    [review_task, weight_task] >> report_task