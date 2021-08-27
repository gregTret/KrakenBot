import os
import time
from TestingModel import * 
from KrakenApi import *
from Handler import *
import subprocess
import shutil

# Kraken API Public and Private Key
# key= yourpublickey
# privateKey= yourprivatekey

# Crypto[=currency Pair to Buy/Sell and Desired Amount
pair=["XMRUSD","ETHUSD"]
minSellAdjustment=[1.01,1.01]
amount=[0.1,0.01]

# Risk Level (1= Very High , 5 = High , 15 = Medium, 30 = Low, 60 = Lowest)
barsToUse=60
# Time Between Request Batches
timeControl=10
# Device used to generate models: by default set to cpu
deviceUsedToModel='cpu'


# Setting Directories up
directory_path = os.getcwd()
# modelLocation=directory_path+'/generatedModels/customModel1030.pth'
modelLocation=directory_path+'/generatedModels/GPU_ETH_TRIPLE_30DPI_60MIN.pth'

testLocation=directory_path+'/tests/tmp.jpeg'
classificationSave=directory_path+'/tests/'

counter=0
while (KrakenStatus()==0):
    for x in range (len(pair)):
        # Time Buffer for Requests
        time.sleep(5)
        # Getting Prices of Currency Pairs
        latest=getCurrentPrice(barsToUse, 'average', pair[x])
        # Converting list to JPEG
        ListToJPEG(latest,testLocation)
        # Classifying Image bassed on Model
        classification=ClassifyImage(modelLocation, testLocation,deviceUsedToModel)
        if (classification==1):
            print (pair[x]+" is Low Currently At (BUY TIME): "+str(latest[len(latest)-1]))
            shutil.move(testLocation, classificationSave+'/buy_' +str(counter)+pair[x]+'.jpeg')
            # Optional Notification When making a purchase/sale
            # subprocess.call(["notify-send",'Testing Notifications',"Go Check Kraken out", '-u','critical'])
            # Making a Market Purchase
            # MarketBuy(key,privateKey,amount[x],pair[x])
            # priceApprox=float(latest[len(latest)-1])*minSellAdjustment[x]
            # priceApprox=round(priceApprox, 2)
            # print ("Bought around: ",str(latest[len(latest)-1]))
            # print ("Selling at: ",str(priceApprox))
            # time.sleep(5)
            # # Making a Limit Sale
            # LimitSell(key,privateKey,amount[x],pair[x],priceApprox)
        elif (classification==2):
             print (pair[x]+" is High Currently At (SELL TIME): "+str(latest[len(latest)-1]))
             shutil.move(testLocation, classificationSave+'/sell_' +str(counter)+pair[x]+'.jpeg')
        else:
            # Not Purchasing, Simply Showing Price
            print ("Current Price of "+pair[x]+":"+str(latest[len(latest)-1]))
            shutil.move(testLocation, classificationSave+'/nothing_' +str(counter)+pair[x]+'.jpeg')
        counter+=1

    minutes=timeControl
    print ("Waiting Until Next Batch for "+str(minutes)+ " Minutes")
    for i in range(minutes):
        time.sleep(60)
        minutes-=1
        print ("Waiting for "+str(minutes)+ " Minutes")


