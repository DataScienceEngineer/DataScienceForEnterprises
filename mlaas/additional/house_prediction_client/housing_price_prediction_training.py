import requests
#Training
training_config={'preprocessed_file_path':
                     '/ml_worker/storage/house_prediction/train_processed.csv',
                 'model_generators_object_list':
                     [{'model_id':'1',
                       'model_shortname':'House Price Predictions Training',
                       'python_function':'ml_automation.model_trainers.house_prediction_trainer.HousePredictionTrainer.performModelTraining',
                       'target_model_file_path':'/ml_worker/storage/house_prediction/lasso_regression.pkl',
                       'additional_params':
                           {'features':['MSSubClass','MSZoning','LotArea','LotShape','OverallQual','OverallCond','YearBuilt','YearRemodAdd','MasVnrArea','BsmtFinSF1','1stFlrSF','2ndFlrSF','GrLivArea','BsmtFullBath','FullBath','HalfBath','Functional','Fireplaces','GarageCars','WoodDeckSF','ScreenPorch','GarageYrBlt_na','LotFrontage'],
                            'predictor_var':'SalePrice',
                            'scaler_file':'/ml_worker/storage/house_prediction/scaler.pkl'}}]}
response=requests.post('http://localhost:5001/mlAutomation', json=training_config)
print(response.text)

