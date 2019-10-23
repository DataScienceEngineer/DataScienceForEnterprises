from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
import time
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2018, 9, 13),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'hello_world2', default_args=default_args, schedule_interval=None)

def print_context():
    with open('/storage/1.txt','a') as a:
        a.write("Executed"+str(datetime.now()))
    return 'Whatever you return gets printed in the logs'
    
def task1():
    time.sleep(15)
    return 'task1'

def task2():
    time.sleep(20)
    return 'task2'

def joinTask(**context):
    print("Hi")
    ti = context['ti']
    print("task1: ",ti.xcom_pull(task_ids='task1'))
    print("task2: ",ti.xcom_pull(task_ids='task2'))
    return None



t1 = PythonOperator(
    task_id='print_the_context',
    python_callable=print_context,
    dag=dag)
t2 = PythonOperator(
    task_id='task1',
    python_callable=task1,
    dag=dag)
t3 = PythonOperator(
    task_id='task2',
    python_callable=task2,
    dag=dag)
t4 = PythonOperator(
    task_id='joinTask',
    python_callable=joinTask,
    provide_context=True,
    dag=dag)
t1>>t2
t1>>t3
t2>>t4
t3>>t4