import wget

def composeTargetUrl(name):
    #https://query1.finance.yahoo.com/v7/finance/download/GOOG?period1=1549564929&period2=1581100929&interval=1d&events=history&crumb=VXUg44197Yq

    baseAddress = "https://query1.finance.yahoo.com/v7/finance/download/"
    startPeriod = "1549564929"
    endPeriod = "1581100929"
    interval = "1d"
    secret = "VXUg44197Yq"
    
    return baseAddress + name + "?period1=" + startPeriod + "&period2=" + endPeriod + "&interval=" + interval + "&events=history&crumb=" + secret
    

name = "NOK"
addr = composeTargetUrl(name)

print("Downloading ");
wget.download(addr, "./history/" + name + ".csv")

print("Done");
