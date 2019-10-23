import requests
#Perform Data Preprocessing
testing_data_processing_config={'raw_file_paths':
                                     {'1':'/ml_worker/storage/house_prediction/test.csv'},
                                 'processed_data_file_path':'/ml_worker/storage/house_prediction/test_processed.csv',
                                 'data_processing_object_list':
                                     [{'data_process_id':'1',
                                       'data_process_shortname':'House Price Predictions Testing Data Processing',
                                       'python_function':'ml_automation.data_processing.house_prediction_data_processor.HousePredictionDataProcessor.performPreprocessing',
                                       'additional_params':
                                           {'features':['MSSubClass','MSZoning','LotArea','LotShape','OverallQual','OverallCond','YearBuilt','YearRemodAdd','MasVnrArea','BsmtFinSF1','1stFlrSF','2ndFlrSF','GrLivArea','BsmtFullBath','FullBath','HalfBath','Functional','Fireplaces','GarageCars','WoodDeckSF','ScreenPorch','GarageYrBlt_na','LotFrontage'],
                                            'catvars':['MSZoning','LotShape','Functional'],
                                            'catvarspredictor':['MSZoning','LotShape','Functional','SalePrice'],
                                            'temporalvars':['YearBuilt','YearRemodAdd'],
                                            'temporalvarspredictor':['YearBuilt','YearRemodAdd','YrSold'],
                                            'basevar':'YrSold',
                                            'numvars':['MSSubClass','LotArea','OverallQual','OverallCond','MasVnrArea','BsmtFinSF1','1stFlrSF','2ndFlrSF','GrLivArea','BsmtFullBath','FullBath','HalfBath','Fireplaces','GarageCars','WoodDeckSF','ScreenPorch','LotFrontage'],
                                            'extravar':'GarageYrBlt_na',
                                            'extra_new_var':'GarageYrBlt',
                                            'skewedvars':['LotFrontage','LotArea','1stFlrSF','GrLivArea','SalePrice'],
                                            'predictor_var':'SalePrice',
                                            'scaler_file':'/ml_worker/storage/house_prediction/scaler.pkl',
                                            'json_files':{
                                                'categorical_frequency_labels':'/ml_worker/storage/house_prediction/catfreqlabels.json',
                                                'ordinal_labels':'/ml_worker/storage/house_prediction/ordinal_labels.json',
                                                'mean_values':'/ml_worker/storage/house_prediction/meanvals.json'},
                                            'type':'predict'}}]}
response=requests.post('http://localhost:5001/mlAutomation', json=testing_data_processing_config)
print(response.text)