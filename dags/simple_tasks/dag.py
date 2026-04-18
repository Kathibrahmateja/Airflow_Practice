"""
Simple task dependency DAG example.
Demonstrates basic Airflow concepts like task dependencies and PythonOperators.
"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def task1():
    """First task - prints a message."""
    print("This is task 1")

def task2():
    """Second task - prints a message."""
    print("This is task 2")

dag = DAG(
    'task_dependency',
    start_date=datetime(2023, 1, 1),
    schedule='@daily',
    catchup=False,
    tags=['examples', 'simple']
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

# Set task dependency: task1 must complete before task2
task1_op >> task2_op
