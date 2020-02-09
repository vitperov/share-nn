# -*- coding: utf-8 -*-

import numpy

from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.models import model_from_json
from tensorflow.python.client import device_lib
from keras import backend as K

def scaleInputData(X, Y):
    Xout = numpy.copy(X)
    Yout = numpy.copy(Y)
    
    print("x=", len(X), "; Y=", len(Y))
    
    for i in range(len(Xout)):
        maxX = numpy.max(Xout[i])
        maxValue = max(maxX, Yout[i])
        
        Xout[i] = Xout[i] / maxValue
        Yout[i] = Yout[i] / maxValue
        
    return [Xout, Yout]

datasets = dict()
datasets = numpy.load("binaryData/predictNdaysToLearn.npy", allow_pickle=True)[()]

X = datasets['X']
Y = datasets['Y']

#[Xout, Yout] = scaleInputData(X, Y)
[Xout, Yout] = [X, Y]

firstLayerInputs = X.shape[1]

model = Sequential()
model.add(Dense(firstLayerInputs, input_dim=firstLayerInputs, activation='linear'))
model.add(Dense(50, activation='sigmoid'))
model.add(Dense(1, activation='sigmoid'))

model.compile(loss="mean_squared_error", optimizer="RMSprop", metrics=['accuracy'])
model.fit(Xout, Yout, epochs = 200, batch_size=30)

scores = model.evaluate(Xout, Yout)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

#save model
outFile="binaryData/predictNdaysToLearn"
json_string = model.to_json()
text_file = open(outFile+".mod", "w")
text_file.write(json_string)
text_file.close()

model.save_weights(outFile+".ntw")
