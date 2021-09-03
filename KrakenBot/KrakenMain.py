print ("Importing packages please wait...")
from os import walk
import time
import shutil
from .KrakenApi import KrakenApiRequests as ka
from .Helper import HelperFunctions as hp
from .TestingModel import TestingModel as tm

class KrakenController():
    def evaluationMode(pair,barsToUse,timeControl,testLocation,classificationSave,modelLocation,deviceUsedToModel,counter):
        while (ka.KrakenStatus()==0):
            for x in range (len(pair)):
                # Getting Prices of Currency Pairs
                latest=ka.getCurrentPrice(barsToUse, 'average', pair[x])
                # Converting list to JPEG
                hp.ListToJPEG(latest,testLocation)
                # Classifying Image bassed on Model
                classification=tm.ClassifyImage(modelLocation, testLocation,deviceUsedToModel)
                if (classification==1):
                    print (pair[x]+" is Low Currently At (BUY TIME): "+str(latest[len(latest)-1]))
                    shutil.move(testLocation, classificationSave+'/buy/' +str(counter)+pair[x]+'.jpeg')
                elif (classification==2):
                    print (pair[x]+" is High Currently At (SELL TIME): "+str(latest[len(latest)-1]))
                    shutil.move(testLocation, classificationSave+'/sell/' +str(counter)+pair[x]+'.jpeg')
                else:
                    print ("Current Price of "+pair[x]+":"+str(latest[len(latest)-1]))
                    shutil.move(testLocation, classificationSave+'/nothing/' +str(counter)+pair[x]+'.jpeg')
                counter+=1
                print (counter)
            minutes=timeControl
            print ("Waiting Until Next Batch for "+str(minutes)+ " Minutes")
            for i in range(minutes):
                time.sleep(60)
                minutes-=1
                print ("Waiting for "+str(minutes)+ " Minutes")

    def tradingBot(key,privateKey,pair,amount,minSellAdjustment,barsToUse,timeControl,testLocation,classificationSave,modelLocation,deviceUsedToModel,counter):
         while (ka.KrakenStatus()==0):
            for x in range (len(pair)):
                # Getting Prices of Currency Pairs
                latest=ka.getCurrentPrice(barsToUse, 'average', pair[x])
                # Converting list to JPEG
                hp.ListToJPEG(latest,testLocation)
                # Classifying Image bassed on Model
                classification=tm.ClassifyImage(modelLocation, testLocation,deviceUsedToModel)
                # Update me---------------------------------------------------------------------
                if (classification==1):
                    print (pair[x]+" is Low Currently At (BUY TIME): "+str(latest[len(latest)-1]))
                    shutil.move(testLocation, classificationSave+'/buy/' +str(counter)+pair[x]+'.jpeg')
                    # Making a Market Purchase
                    ka.MarketBuy(key,privateKey,amount[x],pair[x])
                    priceApprox=float(latest[len(latest)-1])*minSellAdjustment[x]
                    priceApprox=round(priceApprox, 2)
                    print ("Bought around: ",str(latest[len(latest)-1]))
                    print ("Selling at: ",str(priceApprox))
                    time.sleep(5)
                    # Making a Limit Sale 
                    ka.LimitSell(key,privateKey,amount[x],pair[x],priceApprox)
                elif (classification==2):
                    print (pair[x]+" is High Currently At (SELL TIME): "+str(latest[len(latest)-1]))
                    shutil.move(testLocation, classificationSave+'/sell/' +str(counter)+pair[x]+'.jpeg')
                else:
                    # Not Purchasing, Simply Showing Price
                    print ("Current Price of "+pair[x]+":"+str(latest[len(latest)-1]))
                    shutil.move(testLocation, classificationSave+'/nothing/' +str(counter)+pair[x]+'.jpeg')
                # Update me---------------------------------------------------------------------
                counter+=1
                print (counter)

            minutes=timeControl
            print ("Waiting Until Next Batch for "+str(minutes)+ " Minutes")
            for i in range(minutes):
                time.sleep(60)
                minutes-=1
                print ("Waiting for "+str(minutes)+ " Minutes")