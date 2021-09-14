print ("Importing packages please wait...")
from os import walk
import time
import shutil
from .KrakenApi import KrakenApiRequests as ka
from .Helper import HelperFunctions as hp
from .TestingModel import TestingModel as tm

class KrakenController():
    def evaluationMode(pair,barsToUse,timeControl,testLocation,classificationSave,modelLocation,deviceUsedToModel,counter):
        hp.CreateImageFolders(classificationSave)
        while (ka.KrakenStatus()==0):
            for x in range (len(pair)):
                latest=ka.getCurrentPrice(barsToUse, 'average', pair[x])
                hp.ListToJPEG(latest,testLocation)
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

    def tradingBot(key,privateKey,pair,amount,minSellAdjustment,maximumHoldingsValue,barsToUse,timeControl,testLocation,classificationSave,modelLocation,logFileLocation,holdingSummaryLocation,deviceUsedToModel,counter):
         hp.CreateImageFolders(classificationSave)
         while (ka.KrakenStatus()==0):
            for x in range (len(pair)):
                latest=ka.getCurrentPrice(barsToUse, 'average', pair[x])
                hp.ListToJPEG(latest,testLocation)
                classification=tm.ClassifyImage(modelLocation, testLocation,deviceUsedToModel)
                if (classification==1):
                    print (pair[x]+" is Low Currently At (BUY TIME): "+str(latest[len(latest)-1]))
                    shutil.move(testLocation, classificationSave+'/buy/' +str(counter)+pair[x]+'.jpeg')
                    if (KrakenController.holdingsValue(holdingSummaryLocation)<maximumHoldingsValue):
                        if (KrakenController.approvePurchase(pair[x],holdingSummaryLocation)==1):
                            ka.MarketBuy(key,privateKey,amount[x],pair[x])
                            KrakenController.updateMainLog('BUY',pair[x],amount[x],logFileLocation)
                            KrakenController.logPurchase(pair[x],amount[x],holdingSummaryLocation)
                            priceApprox=float(latest[len(latest)-1])*minSellAdjustment[x]
                            priceApprox=round(priceApprox, 2)
                            print ("Bought around: ",str(latest[len(latest)-1]))
                    else:
                        print ("Reached Maximum holdings Value, Will not purchase more...")
                elif (classification==2):
                    print (pair[x]+" is High Currently At (SELL TIME): "+str(latest[len(latest)-1]))
                    shutil.move(testLocation, classificationSave+'/sell/' +str(counter)+pair[x]+'.jpeg')
                    if (KrakenController.approveSale(pair[x],minSellAdjustment[x],holdingSummaryLocation)==1):
                        amountToSell=KrakenController.getHoldingAmount(pair[x],holdingSummaryLocation)
                        amountToSell=(round(amountToSell, 2))
                        ka.MarketSell(key,privateKey,amountToSell,pair[x])
                        KrakenController.updateMainLog('SELL',pair[x],amountToSell,logFileLocation)
                        KrakenController.logSale(pair[x],amountToSell,holdingSummaryLocation)
                        print ("Sold Around: ",str(latest[len(latest)-1]))
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

    def updateMainLog(action,pair,amount,logFileLocation):
        lastPrice=ka.getCurrentPrice(1, 'lastOnly', pair)
        data=str(action)+','+str(pair)+','+str(lastPrice)+','+str(amount)
        hp.appendLineToFile(logFileLocation,data)
    
    def logPurchase(pair,amount,holdingSummaryLocation):
        holdings=[]
        exists=0
        lastPrice=ka.getCurrentPrice(1, 'lastOnly', pair)
        data=hp.holdingCheck(holdingSummaryLocation)
        for x in range(len(data)):
            if(data[x].split(',')[0]==pair):
                exists=1
                amountHeld=float(data[x].split(',')[1])
                cost=float(data[x].split(',')[2])
                cost=amountHeld*cost
                newAmount=float(amount)
                newCost=float(lastPrice)*newAmount
                newCost+=cost
                newAmount=newAmount+amountHeld
                newCost=newCost/newAmount
                result=str(pair)+','+str(newAmount)+','+str(newCost)
                holdings.append(result)
            else:
                holdings.append(data[x])
        if (exists==0):
            result=str(pair)+','+str(amount)+','+str(lastPrice)
            holdings.append(result)
        hp.ltf(holdingSummaryLocation,holdings)
    
    def logSale(pair,amount,holdingSummaryLocation):
        holdings=[]
        data=hp.holdingCheck(holdingSummaryLocation)
        for x in range(len(data)):
            if(data[x].split(',')[0]==pair):
                amountHeld=float(data[x].split(',')[1])
                cost=float(data[x].split(',')[2])
                newAmount=amountHeld-float(amount)
                result=str(pair)+','+str(newAmount)+','+str(cost)
                # holdings.append(result)
            else:
                holdings.append(data[x])
        hp.ltf(holdingSummaryLocation,holdings)
    
    def approvePurchase(pair,holdingSummaryLocation):
        lastPrice=ka.getCurrentPrice(1, 'lastOnly', pair)
        data=hp.holdingCheck(holdingSummaryLocation)
        for x in range(len(data)):
            if(data[x].split(',')[0]==pair):
                cost=float(data[x].split(',')[2])
                if (lastPrice>=cost*0.985):
                    return 0
        return 1

    def approveSale(pair,minimumProfit,holdingSummaryLocation):
        entryExists=0
        lastPrice=ka.getCurrentPrice(1, 'lastOnly', pair)
        data=hp.holdingCheck(holdingSummaryLocation)
        for x in range(len(data)):
            if(data[x].split(',')[0]==pair):
                entryExists=1
                cost=float(data[x].split(',')[2])
                if (lastPrice<=cost*minimumProfit):
                    return 0
        if (entryExists==1):
            return 1
        else:
            return 0
    
    def getHoldingAmount(pair,holdingSummaryLocation):
        data=hp.holdingCheck(holdingSummaryLocation)
        for x in range(len(data)):
            if(data[x].split(',')[0]==pair):
                return(float(data[x].split(',')[1]))
    
    def holdingsValue(holdingSummaryLocation):
        data=hp.holdingCheck(holdingSummaryLocation)
        total=0
        for x in range(len(data)):
            try:
                rowCost=float(data[x].split(',')[1])*float(data[x].split(',')[2])
                total+=rowCost
            except:
                total+=0
        return total