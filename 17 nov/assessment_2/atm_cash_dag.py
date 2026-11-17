cat > atm_cash_dag.py <<'EOF'
import csv

from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


# TASK 1: Load ATM records
def load_atms():
    with open('/opt/airflow/dags/atm_cash.csv', newline='') as file:
        records = list(csv.DictReader(file))

    print('ATM records loaded:', len(records))

    return records


# TASK 2: Identify ATMs with low cash
def identify_low_cash(ti):
    records = ti.xcom_pull(task_ids='load_atms')

    low_cash_atms = []

    for atm in records:
        cash = int(atm['cash_available'])
        demand = int(atm['daily_demand'])

        if cash < demand:
            low_cash_atms.append(atm['atm_id'])

    print('Low cash ATMs:', low_cash_atms)

    return low_cash_atms


# TASK 3: Calculate total available cash
def calculate_total_cash(ti):
    records = ti.xcom_pull(task_ids='load_atms')

    total_cash = 0

    for atm in records:
        total_cash += int(atm['cash_available'])

    print('Total available cash:', total_cash)

    return total_cash


# TASK 4: Generate final report
def generate_report(ti):

    records = ti.xcom_pull(task_ids='load_atms')

    low_cash_atms = ti.xcom_pull(
        task_ids='identify_low_cash'
    )

    total_cash = ti.xcom_pull(
        task_ids='calculate_total_cash'
    )

    print('========== ATM CASH REPLENISHMENT REPORT ==========')

    print('Total number of ATMs:', len(records))

    print('Low cash ATM IDs:', low_cash_atms)

    print('Total available cash:', total_cash)

    print('===================================================')


# Define DAG
with DAG(
    dag_id='atm_cash_pipeline',
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False
) as dag:

    task_load = PythonOperator(
        task_id='load_atms',
        python_callable=load_atms
    )

    task_low_cash = PythonOperator(
        task_id='identify_low_cash',
        python_callable=identify_low_cash
    )

    task_total_cash = PythonOperator(
        task_id='calculate_total_cash',
        python_callable=calculate_total_cash
    )

    task_report = PythonOperator(
        task_id='generate_report',
        python_callable=generate_report
    )

    # Task dependencies
    task_load >> [task_low_cash, task_total_cash]

    [task_low_cash, task_total_cash] >> task_report

EOF