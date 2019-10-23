import pandas as pd
from sklearn.externals import joblib
from sklearn.pipeline import Pipeline
from sklearn_pandas import DataFrameMapper
from prediction_service.algorithms import CustomAlgorithm
import os
#Initialize model for DummyClassifier
model=CustomAlgorithm.DummyClassifier()
#Create features mapping
mapper = DataFrameMapper([
    ('feature1', CustomAlgorithm.Transform1()),
    ('feature2', CustomAlgorithm.Transform2())
])
#Make pipeline
pipeline = Pipeline(
    [("mapper", mapper),("model", model)]
)
#Fitting the pipeline
pipeline.fit(pd.DataFrame([{"feature1":45,"feature2":32},{"feature1":45,"feature2":32}]),pd.DataFrame([{"labels":1},{"labels":2}]))
#Saving the pipeline
if not os.path.exists(r"E:\ml_resources\storage\custom_algorithm"):
    os.makedirs(r"E:\ml_resources\storage\custom_algorithm")
joblib.dump(pipeline,"E:\ml_resources\storage\custom_algorithm\custom_algo.pkl")
#Load the pipeline for local testing
pipeline=joblib.load("E:\ml_resources\storage\custom_algorithm\custom_algo.pkl")
print(pipeline.predict(pd.DataFrame([{"feature1":20,"feature2":12}])))
print(pipeline.predict_proba(pd.DataFrame([{"feature1":20,"feature2":12}])))
print(hasattr(pipeline.named_steps['model'],'xyz'))