# -*- coding: utf-8 -*-

import numpy

from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.models import model_from_json
from tensorflow.python.client import device_lib
from keras import backend as K

def simpleWithVolumeInputData(X, Y):
    Xout = []
    Yout = numpy.copy(Y)
    
    numbersPerDay = 5
    days = int(len(X[0]) / numbersPerDay)
    openPriceIdx = 0
    minPriceIdx = 1
    maxPriceIdx = 2
    closePriceIdx = 3
    volumeIdx = 4
    
    maxVolume = 500e6
    
    for i in range(len(X)):
        row = []
        percentRow=[]
        lastDayClose = 0
        for day in range(1,days):
            prevDayOpen = X[i, day*numbersPerDay + openPriceIdx - 1]
            curDayOpen = X[i, day*numbersPerDay + openPriceIdx]
            openPercent = (curDayOpen - prevDayOpen) / prevDayOpen
            row.append(openPercent)
            
            prevDayClose = X[i, day*numbersPerDay + closePriceIdx - 1]
            curDayClose = X[i, day*numbersPerDay + closePriceIdx]
            lastDayClose = curDayClose
            percent = (curDayClose - prevDayClose) / prevDayClose
            row.append(percent)
            
            curDayMin = X[i, day*numbersPerDay + minPriceIdx]
            curDayMax = X[i, day*numbersPerDay + maxPriceIdx]
            dmin = abs(curDayMin-curDayClose)
            dmax = abs(curDayMax-curDayClose)
            maxD = max(dmin, dmax)
            row.append(maxD/curDayClose)
            
            volume = X[i, day*numbersPerDay + volumeIdx]
            volume = volume / maxVolume
            row.append(volume)

        Yout[i] = (Y[i] - lastDayClose) / lastDayClose

        Xout.append(numpy.array(row))
        
    return [numpy.array(Xout), Yout]
    
datasets = dict()
datasets = numpy.load("binaryData/predictNdaysToLearn.npy", allow_pickle=True)[()]

X = datasets['X']
Y = datasets['Y']

#[Xout, Yout] = simplifyInputData(X, Y)
#[Xout, Yout] = inputDataCalcPercent(Xout, Yout)

[Xout, Yout] = simpleWithVolumeInputData(X, Y)

#Xout[:,1:49] = 0

print("Xout=", Xout)
print("Shape=", Xout.shape)
print("Yout=", Yout)

#exit(0)

firstLayerInputs = Xout.shape[1]

model = Sequential()
model.add(Dense(firstLayerInputs, input_dim=firstLayerInputs, activation='tanh'))
model.add(Dense(15, activation='linear'))
#model.add(Dense(3, activation='linear'))
model.add(Dense(1, activation='tanh'))

model.compile(loss="mean_squared_error", optimizer="Adagrad", metrics=['accuracy'])
model.fit(Xout, Yout, epochs = 1000, batch_size=50)

scores = model.evaluate(Xout, Yout)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))


print("Saving model...")
#save model
outFile="binaryData/predictNdaysToLearn"
json_string = model.to_json()
text_file = open(outFile+".mod", "w")
text_file.write(json_string)
text_file.close()

model.save_weights(outFile+".ntw")

print("Evaluating test set...")

atasets = dict()
datasets = numpy.load("binaryData/predictNdaysToLearn.npy", allow_pickle=True)[()]

X = datasets['X']
Y = datasets['Y']

[Xout, Yout] = simpleWithVolumeInputData(X, Y)

yToTest = model.predict(Xout)
yToTest = numpy.array(yToTest.transpose()[0], dtype="float_")

xLastDayClosePrice = X[:,-2]
yRestored = xLastDayClosePrice * (1+yToTest)
relativeError = (Y-yRestored)/Y
avgError = numpy.sum(numpy.abs(relativeError)) / len(Y) * 100

print("test=", yRestored)
print("relativeError=", relativeError)
print("avgError=", avgError, "%")
