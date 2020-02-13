# -*- coding: utf-8 -*-

import configparser
import matplotlib.pyplot as plt
from keras.models import model_from_json
from common import *

configFile = "settings/teachSettings.ini"

config = configparser.ConfigParser()
config.read(configFile)
name = config['testGraph']['plotQuote']
predictWindow = int(config['predictNdays']['windowSize'])
predictDaysForward = int(config['predictNdays']['daysForward'])

allData = getQuoteAllData(name)

openPriceIdx = 0
minPriceIdx = 1
maxPriceIdx = 2
closePriceIdx = 3
volumeIdx = 4

sOpen = allData[:,openPriceIdx]
sClose = allData[:,closePriceIdx]
sMin = allData[:,minPriceIdx]
sMax = allData[:,maxPriceIdx]
volume = allData[:,volumeIdx]

xDays = range(len(sClose))


with open("binaryData/predictNdaysToLearn.mod", 'r') as content_file:
    json_string = content_file.read()
    
model = model_from_json(json_string)    
model.load_weights("binaryData/predictNdaysToLearn.ntw")

openChange = (sOpen[1:] - sOpen[:-1]) / sOpen[:-1]
closeChange = (sClose[1:] - sClose[:-1]) / sClose[:-1]
minMaxDelta = (sMax[1:] - sMin[1:]) / sClose[1:]
maxVolume = 500e6
volumeNormalized = volume[1:] / maxVolume
feedMatrix = numpy.matrix([openChange, closeChange, minMaxDelta, volumeNormalized]).transpose()

xPredict=[]
yPredict=[]
yNN=[]

predictStep = 2
#predictNumber = int((len(xDays) - predictdaysForward - predictWindow) / predictStep)

for dataIdx in range(predictWindow, len(xDays) - predictDaysForward - predictWindow, predictStep):
    #print("dataIdx=",dataIdx)
    firstDayIdx=dataIdx
    lastDayIdx=dataIdx+predictWindow-1
    
    xData = feedMatrix[firstDayIdx:lastDayIdx, :]
    #print("before flattenin=", xData)
    xData = xData.flatten()
    #print("after flattenin=", xData)
    
    yData = model.predict(xData)
    yData = numpy.array(yData.transpose()[0], dtype="float_")
    yNN.append(yData)
    
    xPredict.append(lastDayIdx-1)
    yPredict.append(numpy.nan)
    
    lastDayClose = sClose[lastDayIdx]
    xPredict.append(lastDayIdx)
    yPredict.append(lastDayClose)
    
    yRestored = lastDayClose * (1+yData)
    xPredict.append(lastDayIdx+1)
    yPredict.append(yRestored)
    
xPredict = numpy.array(xPredict)
yPredict = numpy.array(yPredict)

fig = plt.figure()
sQ = fig.add_subplot(111)
#sNN = fig.add_subplot(212)

sQ.plot(xDays, sClose)
sQ.plot(xPredict, yPredict)
#sQ.plot(sMin)
#sQ.plot(sMax)

#sNN.plot(numpy.array(yNN))

plt.show()
