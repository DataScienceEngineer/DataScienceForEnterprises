import requests
def call(testFeatures,filename,implementation,requestArguments=None):
    print("Invoking Real time Prediction Engine with " + implementation)
    testData = {}
    testData['payload'] = testFeatures
    testData['pipelineFilename'] = filename
    testData['implementation'] = implementation
    if requestArguments is not None:
        testData['requestArguments'] = requestArguments
    print(testData)
    return requests.post('http://localhost:8080/invocations', json=testData)

#Case 1: Generic Scikit Learn Algorithm
filename1='/s3-file-storage/logistic_regression/iris.pickle'
testFeatures1 = [{'sepal_length':5.1,'sepal_width':3.5,'petal_length':1.4,'petal_width':0.2},{'sepal_length':2.1,'sepal_width':5.5,'petal_length':6.4,'petal_width':0.2}]
#print(call(testFeatures1,filename1,'Logistic Regresssion').text)

#Case 2: Custom Machine Learning Algorithm
filename2='custom_algorithm/custom_algo.pkl'
testFeatures2= [{"feature1":20,"feature2":12}]
print(call(testFeatures2,filename2,'Custom Algorithm').text)

#Case 3: Keras Machine Learning Algorithm
filename2='dnn_keras/keras_pipeline.pkl'
requestArguments={'modelFilename': 'dnn_keras/keras_model.h5'}
testFeatures2= [{"feature1":20,"feature2":12,"feature3":33}]
#print(call(testFeatures2,filename2,'Keras',requestArguments).text)


