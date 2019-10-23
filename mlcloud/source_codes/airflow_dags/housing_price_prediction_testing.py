# python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable
import time
import requests
import ast
import os
import pandas as pd
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
    'housing_price_prediction_testing', default_args=default_args, schedule_interval=None,catchup=False)

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
    
def testing_data_processing():
    testing_data_processing_config =ast.literal_eval(Variable.get("testing_data_processing_config"))
    print(invoke_endpoint(testing_data_processing_config))
    
def testing_model():
    testing_config =ast.literal_eval(Variable.get("testing_config"))
    print(invoke_endpoint(testing_config))
    
def pull_predicted_labels():
    fetch_output_data =ast.literal_eval(Variable.get("fetch_output_data"))
    response=invoke_endpoint(fetch_output_data)
    output_dict=ast.literal_eval(response['1:Fetch Housing Price Prediction Outputs']['message'])
    output_df=pd.DataFrame(output_dict)
    outdir='/storage/housing_price_prediction'
    if not os.path.exists(outdir):
       os.mkdir(outdir)
    output_df.to_csv(str(outdir+'/predout.csv'))

def pull_test_data():
    fetch_test_data =ast.literal_eval(Variable.get("fetch_test_data"))
    response=invoke_endpoint(fetch_test_data)
    output_dict=ast.literal_eval(response['1:Fetch Housing Price Test Data']['message'])
    output_df=pd.DataFrame(output_dict)
    outdir='/storage/housing_price_prediction'
    if not os.path.exists(outdir):
       os.mkdir(outdir)
    output_df.to_csv(str(outdir+'/test.csv'))
    
t1 = PythonOperator(
    task_id='testing_data_processing',
    python_callable=testing_data_processing,
    dag=dag)

t2 = PythonOperator(
    task_id='testing_model',
    python_callable=testing_model,
    dag=dag)

t3 = PythonOperator(
    task_id='pull_predicted_labels',
    python_callable=pull_predicted_labels,
    dag=dag)
    
t4 = PythonOperator(
    task_id='pull_test_data',
    python_callable=pull_test_data,
    dag=dag)

t1>>t2>>t3
t2>>t4
