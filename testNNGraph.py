# -*- coding: utf-8 -*-

import configparser
import matplotlib.pyplot as plt
from common import *

configFile = "settings/teachSettings.ini"

config = configparser.ConfigParser()
config.read(configFile)
name = config['testGraph']['plotQuote']

allData = getQuoteAllData(name)

openPriceIdx = 0
minPriceIdx = 1
maxPriceIdx = 2
closePriceIdx = 3
volumeIdx = 4

sClose = allData[:,closePriceIdx]
sMin = allData[:,minPriceIdx]
sMax = allData[:,maxPriceIdx]

fig = plt.figure()
sQ = fig.add_subplot(111)

sQ.plot(sClose)
#sQ.plot(sMin)
#sQ.plot(sMax)

plt.show()
