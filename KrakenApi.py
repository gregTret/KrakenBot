import requests
import json
import pandas as pd
import time
import matplotlib.pyplot as plt

#Get current status of Kraken API
def KrakenStatus():
    fail=1
    while (fail==1):
        try:
            resp = requests.get('https://api.kraken.com/0/public/SystemStatus')
            res=(resp.json()['result']['status'])
            fail=0
        except:
            print ("Failed to get Kraken Status, trying again")
            fail=1
            pass
        time.sleep(5)
    if (res=="online"):
        return 0
    elif (res=="post_only"):
        return 1
    elif (res=="cancel_only"):    
        return 2
    else:
        return 3

#Get Current Trade data (Time interval to use/Columns to return)
def getCurrentPrice(selection,dataToReturn,currencyPair):
    data=[]
    selection=str(selection)
    url="https://api.kraken.com/0/public/OHLC?pair="
    url+=currencyPair
    url+="&interval="
    url+=selection
    fail=1
    while (fail==1):
        try:
            resp = requests.get(url) 
            fail=0
        except:
            print ("Failed to get Data, trying again")
            fail=1
            pass 
        time.sleep(5)
    nickname= str(resp.json()['result'])
    nickname=nickname.split('\'')
    for x in (resp.json()['result'][nickname[1]]):
        data.append(x)
    if (dataToReturn=='all'):
        return data
    elif (dataToReturn=='high'):
        alt=[]
        for x in range (len(data)):
            alt.append(float(data[x][2]))
        return alt
    elif (dataToReturn=='low'):
        alt=[]
        for x in range (len(data)):
            alt.append(float(data[x][3]))
        return alt
    elif (dataToReturn=='average'):
        alt=[]
        for x in range (len(data)):
            alt.append((float(data[x][2])+float(data[x][2]))/2)
        return alt

def ListToJPEG(data,filename):
    newData=[]
    for i in range(len(data)):
        if (i>=(len(data)-101)):
            newData.append(data[i])
    df = pd.DataFrame(newData, columns=['data'])
    df.data.plot()
    plt.savefig(filename,dpi=30)
    plt.clf()