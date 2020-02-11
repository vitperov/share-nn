# -*- coding: utf-8 -*-

import configparser
import csv
import numpy
import scipy.io
from common import *

def prepareNDaysPredictorData(allData, window, daysForward):
    X = []
    Y = []
    
    maxBlockSize = window + daysForward
    N = len(allData) - maxBlockSize
    
    for i in range(N):
        matrix = allData[i:i+window]
        X.append(matrix.flatten())
        
        dayClosePrice = allData[i+window+daysForward, 3]
        Y.append(dayClosePrice)
    return [numpy.array(X), numpy.array(Y)]
    
configFile = "settings/teachSettings.ini"

config = configparser.ConfigParser()
config.read(configFile)
quotes = config['default']['learnQuotes']
quotesList = quotes.split()

predictWindow = int(config['predictNdays']['windowSize'])
predictdaysForward = int(config['predictNdays']['daysForward'])

print("List=", quotesList)

Xall = None
Yall = None
for name in quotesList:
    allData = getQuoteAllData(name)
    [X, Y] = prepareNDaysPredictorData(allData, predictWindow, predictdaysForward)
    if Xall is None:
        Xall = X
    else:
        Xall = numpy.append(Xall, X, axis=0)
        
    if Yall is None:
        Yall = Y
    else:
        Yall = numpy.append(Yall, Y, axis=0)

print("Got ", Xall.shape, " points for learning")

datasets = dict()
datasets['X'] = Xall
datasets['Y'] = Yall
numpy.save("binaryData/predictNdaysToLearn.npy", datasets)

#save to Matlab
scipy.io.savemat("binaryData/predictNdaysToLearn.mat", datasets)


testQuotes = config['default']['testQuotes']
testQuotesList = testQuotes.split()
Xall = None
Yall = None
for name in testQuotesList:
    allData = getQuoteAllData(name)
    [X, Y] = prepareNDaysPredictorData(allData, predictWindow, predictdaysForward)
    if Xall is None:
        Xall = X
    else:
        Xall = numpy.append(Xall, X, axis=0)
        
    if Yall is None:
        Yall = Y
    else:
        Yall = numpy.append(Yall, Y, axis=0)

print("Got ", Xall.shape, " points for testing")

datasets = dict()
datasets['X'] = Xall
datasets['Y'] = Yall
numpy.save("binaryData/testNdaysToLearn.npy", datasets)

#save to Matlab
scipy.io.savemat("binaryData/testNdaysToLearn.mat", datasets)
