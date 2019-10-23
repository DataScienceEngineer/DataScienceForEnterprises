from sklearn.datasets import load_iris
import pandas as pd
from sklearn.externals import joblib
from sklearn.pipeline import Pipeline
from sklearn_pandas import DataFrameMapper
from sklearn.linear_model import LogisticRegression
import os
iris = load_iris()
X, y = iris.data, iris.target
df_x=pd.DataFrame(X,columns=['sepal_length','sepal_width','petal_length','petal_width'])
y=pd.DataFrame(y).values.ravel()
#Create features mapping
mapper = DataFrameMapper([('sepal_length',None),('sepal_width',None),('petal_length',None),('petal_width',None)])
clf = LogisticRegression()
#Make pipeline
pipeline = Pipeline ([( "mapper", mapper),("model",clf)])
#Fitting the pipeline
pipeline.fit(df_x,y)
#Saving the pipeline
if not os.path.exists(r"E:\ml_resources\storage\logistic_regression"):
    os.makedirs(r"E:\ml_resources\storage\logistic_regression")
joblib.dump(pipeline, filename='E:\ml_resources\storage\logistic_regression\iris.pickle')
#Load the pipeline for local testing
pipline=joblib.load('E:\ml_resources\storage\logistic_regression\iris.pickle')
#Check the results
print(pipeline.predict(pd.DataFrame([{'sepal_length':5.1,'sepal_width':3.5,'petal_length':1.4,'petal_width':0.2}])))

