# -*- coding: utf-8 -*-

import configparser
import csv
import numpy

def getQuoteAllData(name):
    rawData = []
    with open("history/"+name+".txt", 'r') as csvfile:
        rows = csv.reader(csvfile, delimiter=',')
        for row in rows:
            if "TICKER" in row[0]:
                continue
            filtered = numpy.array(row)
            filtered = filtered[4:]
            rawData.append(filtered)
    cleanData = numpy.array(rawData, dtype='f')
    print("array=", cleanData)
    return cleanData

def prepareNDaysPredictorData(allData, window, daysForward):
    X = []
    Y = []
    
    maxBlockSize = window + daysForward
    N = len(allData) - maxBlockSize
    
    print("allData=", len(allData), "; N=", N)
    
    for i in range(N):
        matrix = allData[i:i+window]
        X.append(matrix.flatten())
        
        dayClosePrice = allData[i+window+daysForward, 3]
        Y.append(dayClosePrice)
    return [numpy.array(X), numpy.array(Y)]
    
configFile = "teachSettings.ini"

config = configparser.ConfigParser()
config.read(configFile)
quotes = config['default']['learnQuotes']
quotesList = quotes.split()

predictWindow = int(config['predictNdays']['windowSize'])
predictdaysForward = int(config['predictNdays']['daysForward'])

print("List=", quotesList)

allData = getQuoteAllData(quotesList[0])
[X, Y] = prepareNDaysPredictorData(allData, predictWindow, predictdaysForward)

#print("X=", X)
#print("Y=", Y)
