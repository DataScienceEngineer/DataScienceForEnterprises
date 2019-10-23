import requests
#Testing
testing_config={'preprocessed_file_path':'/ml_worker/storage/house_prediction/test_processed.csv',
                 'model_predictors_object_list':
                     [{'task_id':'1',
                       'task_shortname':'House Price Predictions Testing',
                       'model_file_paths':{'lasso_file':'/ml_worker/storage/house_prediction/lasso_regression.pkl'},
                       'python_function':'ml_automation.model_predictors.house_prediction_predictor.HousePredictionPredictor.performModelPredictions',
                       'additional_params':
                           {'features':['MSSubClass','MSZoning','LotArea','LotShape','OverallQual','OverallCond','YearBuilt','YearRemodAdd','MasVnrArea','BsmtFinSF1','1stFlrSF','2ndFlrSF','GrLivArea','BsmtFullBath','FullBath','HalfBath','Functional','Fireplaces','GarageCars','WoodDeckSF','ScreenPorch','GarageYrBlt_na','LotFrontage'],
                            'predictor_var':'SalePrice',
                            'scaler_file':'/ml_worker/storage/house_prediction/scaler.pkl'},
                       'target_file_path':'/ml_worker/storage/house_prediction/predout.csv'}]}

response=requests.post('http://localhost:5001/mlAutomation', json=testing_config)
print(response.text)

