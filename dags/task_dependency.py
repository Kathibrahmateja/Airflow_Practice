from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def task1():
    print("This is task 1")

def task2():
    print("This is task 2")

dag = DAG(
    'task_dependency',
    start_date=datetime(2023, 1, 1),
    schedule='@daily',
    catchup=False
)

task1_op = PythonOperator(
    task_id='task1',
    python_callable=task1,
    dag=dag
)

task2_op = PythonOperator(
    task_id='task2',
    python_callable=task2,
    dag=dag
)

# task2_op.set_upstream(task1_op)
task1_op >> task2_op