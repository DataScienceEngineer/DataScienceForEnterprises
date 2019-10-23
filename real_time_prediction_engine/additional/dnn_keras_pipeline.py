import keras
import pandas as pd
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn import pipeline
from sklearn.externals import joblib
from sklearn_pandas import DataFrameMapper
import ModelDesign
import os
mapper = DataFrameMapper(
[ ('feature1',None),
  ('feature2',None),
  ('feature3',None)
]);

classifier = ModelDesign.model_fn()
classifier = KerasClassifier(build_fn = ModelDesign.model_fn, batch_size = 64, epochs = 2)

pipeline = pipeline.Pipeline([
    ("mapper", mapper),
    ('model', classifier)
])
train=pd.DataFrame([{"feature1":45,"feature2":32,"feature3":33},{"feature1":45,"feature2":32,"feature3":36}])
labels=pd.DataFrame([{"labels":1},{"labels":2}])
test=pd.DataFrame([{"feature1":20,"feature2":12,"feature3":31}])
pipeline.fit(train,labels)
pipeline.predict(test)
if not os.path.exists(r"E:\ml_resources\storage\dnn_keras"):
    os.makedirs(r"E:\ml_resources\storage\dnn_keras")
pipeline.named_steps['model'].model.save('E:\ml_resources\storage\dnn_keras\keras_model.h5')
pipeline.named_steps['model'].model = None
joblib.dump(pipeline, 'E:\ml_resources\storage\dnn_keras\keras_pipeline.pkl')
keras.backend.clear_session()

