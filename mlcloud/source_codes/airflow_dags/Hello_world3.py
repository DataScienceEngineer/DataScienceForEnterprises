# python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
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
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2018, 9, 20),
}

dag = DAG(
    'hello_world3', default_args=default_args, schedule_interval=None,catchup=False)

def print_context():
    print("Hello yoo")
    with open('/storage/hello-world-example/some1.txt','a') as a:
        a.write("Executed now2 yo 1"+str(datetime.now()))
    time.sleep(10)
    return 'Whatever you return gets printed in the logs'


def print_context2():
    with open('/storage/hello-world-example/some1.txt','a') as a:
        a.write("Executed now2 yo 2"+str(datetime.now()))
    time.sleep(15)
    return 'Whatever you return gets printed in the logs'


		
t1 = PythonOperator(
    task_id='print_the_context1',
    python_callable=print_context,
    dag=dag)

t2 = PythonOperator(
    task_id='print_the_context2',
    python_callable=print_context2,
    dag=dag)

	
t2.set_upstream(t1)
