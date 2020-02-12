# -*- coding: utf-8 -*-

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
    return cleanData
    
class Quote:
    def __init__(self, name):
        self.name = name
        self.allData = getQuoteAllData(name)
