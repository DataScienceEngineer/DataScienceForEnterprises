import keras
from keras.models import Sequential
from keras.layers import Dense,Dropout
def model_fn():
    # Initialising the ANN
    classifier = Sequential()
    classifier.add(Dense(1, input_shape=(3,)))
    classifier.compile(optimizer = keras.optimizers.Adam(lr=0.001,decay=1e-5), loss = 'mean_squared_error',metrics=['mean_squared_error'])
    return classifier