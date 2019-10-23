import requests
filename='/s3-file-storage/logistic_regression/iris.pickle'
testData={}
testFeatures = [{'sepal_length':5.1,'sepal_width':3.5,'petal_length':1.4,'petal_width':0.2},{'sepal_length':2.1,'sepal_width':5.5,'petal_length':6.4,'petal_width':0.2}]
testFeatures=testFeatures*1
testData['payload']=testFeatures
testData['pipelineFilename']=filename
testData['implementation']="Decision Tree"
response=requests.post('http://localhost:5001/asyncInvocation', json=testData)
print(response.text)