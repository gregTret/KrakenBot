import os
import time
from TestingModel import * 
from KrakenApi import *
from Handler import *
import subprocess

# Kraken API Public and Private Key
# key= yourpublickey
# privateKey= yourprivatekey

# Crypto[=currency Pair to Buy/Sell and Desired Amount
pair=["XMRUSD","ETHUSD","DOTUSD"]
minSellAdjustment=[1.01,1.01,1.01]
amount=[0.1,0.01,1.00]

# Risk Level (1= Very High , 5 = High , 15 = Medium, 30 = Low, 60 = Lowest)
barsToUse=5
#Time Between Request Batches
timeControl=5

# Setting Directories up
directory_path = os.getcwd()
modelLocation=directory_path+'/generatedModels/customModel1030.pth'
testLocation=directory_path+'/tests/tmp.jpeg'

while (KrakenStatus()==0):
    for x in range (len(pair)):
        # Time Buffer for Requests
        time.sleep(5)
        # Getting Prices of Currency Pairs
        latest=getCurrentPrice(barsToUse, 'average', pair[x])
        # Converting list to JPEG
        ListToJPEG(latest,testLocation)
        # Classifying Image bassed on Model
        if (ClassifyImage(modelLocation, testLocation)==1):
            print (pair[x]+" is Low Currently At: "+str(latest[len(latest)-1]))
            # Optional Notification When making a purchase/sale
            # subprocess.call(["notify-send",'Testing Notifications',"Go Check Kraken out", '-u','critical'])
            # Making a Market Purchase
            MarketBuy(key,privateKey,amount[x],pair[x])
            priceApprox=float(latest[len(latest)-1])*minSellAdjustment[x]
            priceApprox=round(priceApprox, 2)
            print ("Bought around: ",str(latest[len(latest)-1]))
            print ("Selling at: ",str(priceApprox))
            time.sleep(5)
            # Making a Limit Sale
            LimitSell(key,privateKey,amount[x],pair[x],priceApprox)
        else:
            # Not Purchasing, Simply Showing Price
            print ("Current Price of "+pair[x]+":"+str(latest[len(latest)-1]))

    minutes=timeControl
    print ("Waiting Until Next Batch for "+str(minutes)+ " Minutes")
    for i in range(minutes):
        time.sleep(60)
        minutes-=1
        print ("Waiting for "+str(minutes)+ " Minutes")


