import requests
#Fetch Outputs
fetch_outputs={'custom_function_object':
                   {'request_id':'1','request_shortname':'Fetch Housing Price Prediction Outputs',
                    'python_function':'ml_automation.custom_functions.send_dict_from_csvfile.send_dict_from_csvfile.performOperation',
                    'arguments':{'filepath' : '/ml_worker/storage/house_prediction/predout.csv' }}}
response=requests.post('http://localhost:5001/mlAutomation', json=fetch_outputs)
print(response.text)
fetch_outputs={'custom_function_object':
                   {'request_id':'1','request_shortname':'Fetch Housing Price Test Data',
                    'python_function':'ml_automation.custom_functions.send_dict_from_csvfile.send_dict_from_csvfile.performOperation',
                    'arguments':{'filepath' : '/ml_worker/storage/house_prediction/test.csv' }}}
response=requests.post('http://localhost:5001/mlAutomation', json=fetch_outputs)
print(response.text)


