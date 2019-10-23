# python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable
import time
import requests
import ast

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2018, 9, 13),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'housing_price_prediction_training', default_args=default_args, schedule_interval=None,catchup=False)

##MLaaS Job Invocation
def invoke_endpoint(config):
    mlaas_invoke_endpoint=str(Variable.get('MLaaS_endpoint_address')+'mlAutomation')
    mlaas_result_endpoint=str(Variable.get('MLaaS_endpoint_address')+'check/')
    response=requests.post(mlaas_invoke_endpoint, json=config)
    while requests.get(mlaas_result_endpoint+response.text).text=="PENDING":
       time.sleep(1)
    response_str=requests.get(mlaas_result_endpoint+response.text).text
    response_str=response_str.replace('nan','None')
    response=ast.literal_eval(response_str)
    if 'Exception' in response: #Propagate Exception from MLaaS
    	raise Exception("Remote Exception Occurred in MLaaS:: "+str(response["Exception"]))
    return response
    

def training_data_processing():
    training_data_processing_config =ast.literal_eval(Variable.get("training_data_processing_config"))
    print(invoke_endpoint(training_data_processing_config))
    
def training_model():
    training_config =ast.literal_eval(Variable.get("training_config"))
    print(invoke_endpoint(training_config))
    
t1 = PythonOperator(
    task_id='training_data_processing',
    python_callable=training_data_processing,
    dag=dag)

t2 = PythonOperator(
    task_id='training_model',
    python_callable=training_model,
    dag=dag)

t1>>t2
