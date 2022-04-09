print ("Importing packages please wait...")
from os import walk
import time
import shutil
from .KrakenApi import KrakenApiRequests as ka
from .Helper import HelperFunctions as hp
from .TestingModel import TestingModel as tm

class KrakenController():
    def tradingBot(key,privateKey,pair,amount,minSellAdjustment,maximumHoldingsValue,barsToUse,timeControl,testLocation,classificationSave,modelLocation,logFileLocation,holdingSummaryLocation,deviceUsedToModel):
         hp.CreateImageFolders(classificationSave)
         while (ka.KrakenStatus()==0):
            for x in range (len(pair)):
                latest=ka.getCurrentPrice(barsToUse, 'average', pair[x])
                hp.ListToJPEG(latest,testLocation)
                classification=tm.ClassifyImage(modelLocation, testLocation,deviceUsedToModel)
                name=int(1000*time.time())
                if (classification==1):
                    print (pair[x]+" is Low Currently At (BUY TIME): "+str(latest[len(latest)-1]))
                    shutil.move(testLocation, classificationSave+'/buy/' +str(name)+pair[x]+'.jpeg')
                    shutil.move(testLocation.replace(".jpeg",".txt"), classificationSave+'/buy/' +str(name)+pair[x]+'.txt')
                    approximateCost=(amount[x]*latest[len(latest)-1])
                    print ("Approximate Cost of Purchase=",approximateCost)
                    print ("Current holdings Value:",str(KrakenController.holdingsValue(holdingSummaryLocation)))
                    if ((KrakenController.holdingsValue(holdingSummaryLocation)+approximateCost)<maximumHoldingsValue):
                        if (KrakenController.approvePurchase(pair[x],holdingSummaryLocation)==1):
                            ka.MarketBuy(key,privateKey,amount[x],pair[x])
                            KrakenController.updateMainLog('BUY',pair[x],amount[x],logFileLocation)
                            KrakenController.logPurchase(pair[x],amount[x],holdingSummaryLocation)
                            priceApprox=float(latest[len(latest)-1])*minSellAdjustment
                            priceApprox=round(priceApprox, 2)
                            print ("Bought around: ",str(latest[len(latest)-1]))
                    else:
                        print ("Reached or will exceed Maximum holdings Value, Will not purchase more...")
                elif (classification==2):
                    print (pair[x]+" is High Currently At (SELL TIME): "+str(latest[len(latest)-1]))
                    shutil.move(testLocation, classificationSave+'/sell/' +str(name)+pair[x]+'.jpeg')
                    shutil.move(testLocation.replace(".jpeg",".txt"), classificationSave+'/sell/' +str(name)+pair[x]+'.txt')
                    if (KrakenController.approveSale(pair[x],minSellAdjustment,holdingSummaryLocation)==1):
                        amountToSell=KrakenController.getHoldingAmount(pair[x],holdingSummaryLocation)
                        amountToSell=(round(amountToSell, 2))
                        # amountToSell=(round(amountToSell*0.99, 4))
                        ka.MarketSell(key,privateKey,amountToSell,pair[x])
                        KrakenController.updateMainLog('SELL',pair[x],amountToSell,logFileLocation)
                        KrakenController.logSale(pair[x],amountToSell,holdingSummaryLocation)
                        print ("Sold Around: ",str(latest[len(latest)-1]))
                    else:
                        print ("Sale Not Approved")
                else:
                    print ("Current Price of "+pair[x]+":"+str(latest[len(latest)-1]))
                    shutil.move(testLocation, classificationSave+'/nothing/' +str(name)+pair[x]+'.jpeg')
                    shutil.move(testLocation.replace(".jpeg",".txt"), classificationSave+'/nothing/' +str(name)+pair[x]+'.txt')
            minutes=timeControl
            print ("Waiting Until Next Batch for "+str(minutes)+ " Minutes")
            for i in range(minutes):
                time.sleep(60)
                minutes-=1
                print ("Waiting for "+str(minutes)+ " Minutes")

    def singleCycle(key,privateKey,pair,amount,minSellAdjustment,maximumHoldingsValue,barsToUse,timeControl,testLocation,classificationSave,modelLocation,logFileLocation,holdingSummaryLocation,deviceUsedToModel):
        hp.CreateImageFolders(classificationSave)
        returnResult=[]
        if (ka.KrakenStatus()==0):
            for x in range (len(pair)):
                latest=ka.getCurrentPrice(barsToUse, 'average', pair[x])
                hp.ListToJPEG(latest,testLocation)
                classification=tm.ClassifyImage(modelLocation, testLocation,deviceUsedToModel)
                if (classification==1):
                    shutil.move(testLocation, classificationSave+'/buy/' +str(int(1000*time.time()))+pair[x]+'.jpeg')
                    if (KrakenController.holdingsValue(holdingSummaryLocation)<maximumHoldingsValue):
                        if (KrakenController.approvePurchase(pair[x],holdingSummaryLocation)==1):
                            ka.MarketBuy(key,privateKey,amount[x],pair[x])
                            KrakenController.updateMainLog('BUY',pair[x],amount[x],logFileLocation)
                            KrakenController.logPurchase(pair[x],amount[x],holdingSummaryLocation)
                            priceApprox=float(latest[len(latest)-1])*minSellAdjustment
                            priceApprox=round(priceApprox, 2)
                            ret=[]
                            ret.append('Purchased')
                            ret.append(pair[x])
                            ret.append(str(latest[len(latest)-1]))
                            ret.append(amount[x])
                            ret.append('Buy')
                            returnResult.append(ret)      
                    else:
                        ret=[]
                        ret.append('Nothing')
                        ret.append(pair[x])
                        ret.append(str(latest[len(latest)-1]))
                        ret.append(amount[x])
                        ret.append('Buy')
                        returnResult.append(ret)
                elif (classification==2):
                    shutil.move(testLocation, classificationSave+'/sell/' +str(int(1000*time.time()))+pair[x]+'.jpeg')
                    amountToSell=KrakenController.getHoldingAmount(pair[x],holdingSummaryLocation)
                    amountToSell=(round(amountToSell, 2))
                    # amountToSell=amountToSell*0.99
                    if (KrakenController.approveSale(pair[x],minSellAdjustment,holdingSummaryLocation)==1):
                        ka.MarketSell(key,privateKey,amountToSell,pair[x])
                        KrakenController.updateMainLog('SELL',pair[x],amountToSell,logFileLocation)
                        KrakenController.logSale(pair[x],amountToSell,holdingSummaryLocation)
                        ret=[]
                        ret.append('Sold')
                        ret.append(pair[x])
                        ret.append(str(latest[len(latest)-1]))
                        ret.append(amountToSell)
                        ret.append('Sell')
                        returnResult.append(ret)
                    else:
                        ret=[]
                        ret.append('Nothing')
                        ret.append(pair[x])
                        ret.append(str(latest[len(latest)-1]))
                        ret.append(amountToSell)
                        ret.append('Sell')
                        returnResult.append(ret)
                else:
                    ret=[]
                    ret.append('Nothing')
                    ret.append(pair[x])
                    ret.append(str(latest[len(latest)-1]))
                    ret.append(amount[x])
                    ret.append('Nothing')
                    returnResult.append(ret)
                    shutil.move(testLocation, classificationSave+'/nothing/' +str(int(1000*time.time()))+pair[x]+'.jpeg')
        return returnResult


    def newTradingBot(amountsArray,key,privateKey,pairs,minSellAdjustment,maximumHoldingsValue,timeControl,testLocation,classificationSave,modelLocation,logFileLocation,holdingSummaryLocation,deviceUsedToModel):
         hp.CreateImageFolders(classificationSave)

         bars=[1,5,15,60,1440]
         adjustment=1.025
         breakevenAdjustment=1.025
         delayAfterBigPurchase=0
        #  Implement delay after small purchase (5 min?) 

         latestCostArray=[] 
         while (ka.KrakenStatus()==0):
            for pair in range (len(pairs)):
                output=""
                amounts=amountsArray[pair]
                classifications=[]
                holdingPercent=round((KrakenController.holdingsValue(holdingSummaryLocation)/maximumHoldingsValue)*100, 2)
                for bar in range (len(bars)):
                    # Getting Prices
                    latest=ka.getCurrentPrice(bars[bar], 'average', pairs[pair])
                    minimumSell=KrakenController.getAverageCost(pairs[pair],holdingSummaryLocation)
                    amountHeld=KrakenController.getHoldingsAmount(pairs[pair],holdingSummaryLocation)
                    avgCost=KrakenController.getAverageCost(pairs[pair],holdingSummaryLocation)
                    trueAmountSpent=avgCost*amountHeld
                                                            
                    minimumSell=minimumSell*adjustment

                    if (bars[bar]==1):
                        latestCostArray=latest
                        breakeven=KrakenController.getAverageCost(pairs[pair],holdingSummaryLocation)*1.005

                        # Generating Output
                        output+="~~~~~~ "+pairs[pair]+' ~~~~~~\n\n'
                        output+=("Latest Price  : "+ str(round(latestCostArray[len(latestCostArray)-1],2)))+'\n'
                        output+=("Breakeven     : "+(str(round(breakeven,2))))+'\n'
                        output+=("Minimum Sell  : "+str(round(minimumSell,2)))+'\n\n'
                        output+=("Amount Spent  : "+str(round(trueAmountSpent, 2)))+'\n'
                        output+=("Total Held    : "+str(round(amountHeld,2)))+'\n'
                        output+=("Average Cost  : "+ str(round(KrakenController.getAverageCost(pairs[pair],holdingSummaryLocation),2)))+'\n'
                        output+=(("Funds Used    : "+str(holdingPercent)+"%"))+'\n\n'

                        if (amountHeld!=0):
                            # Calculating P/L
                            PL=latestCostArray[len(latestCostArray)-1]/(avgCost*1.005)
                            PL-=1
                            V=PL*trueAmountSpent
                            PL*=100
                            PL=round(PL,2)
                            V=round(V,2)
                            output+=("Profit/Loss   : "+ str(round(PL,3))+'%')+'\n'
                            output+=("Profit/Loss   : "+str(V))+'\n\n'
                        else:
                            output+="No Holdings \n"
                    
                    hp.ListToJPEG(latest,testLocation)
                    classification=tm.ClassifyImage(modelLocation, testLocation,deviceUsedToModel)
                    name=int(1000*time.time())
                    classifications.append(classification)

                    # Saving Classifications
                    if (classification==1):
                        shutil.move(testLocation, classificationSave+'/buy/' +str(name)+pairs[pair]+'.jpeg')
                        shutil.move(testLocation.replace(".jpeg",".txt"), classificationSave+'/buy/' +str(name)+pairs[pair]+'.txt')
                    elif (classification==2):
                        shutil.move(testLocation, classificationSave+'/sell/' +str(name)+pairs[pair]+'.jpeg')
                        shutil.move(testLocation.replace(".jpeg",".txt"), classificationSave+'/sell/' +str(name)+pairs[pair]+'.txt')
                    else:
                        shutil.move(testLocation, classificationSave+'/nothing/' +str(name)+pairs[pair]+'.jpeg')
                        shutil.move(testLocation.replace(".jpeg",".txt"), classificationSave+'/nothing/' +str(name)+pairs[pair]+'.txt')
                
                output+=str(classifications)+'\n'
                KrakenController.print_msg_box('\n'+output,indent=5,width=22)
                # START OF CLASSIFICATIONS
                # print (classifications)

                # Starting off holdings if [0] agrees ONLY if amountHeld==0
                if (amountHeld==0):
                    print ("No Holdings: Buying Small amount to start...")
                    if (classifications[0]==1 or classifications[1]==1): 
                        KrakenController.purchaseImmediate(pairs[pair],amounts[0],logFileLocation,maximumHoldingsValue,holdingSummaryLocation,latestCostArray,key,privateKey)

                # Buying Immediate if [3] or [4] agree
                if ((latestCostArray[len(latestCostArray)-1]<minimumSell) or amountHeld==0):
                    if (delayAfterBigPurchase<=0):
                        if (classifications[4]==1 or classifications[3]==1):
                            print ("[4] or [3] Indicate time to buy-> Making Large Purchase and waiting 30 Minutes")
                            if (KrakenController.purchaseImmediate(pairs[pair],amounts[4],logFileLocation,maximumHoldingsValue,holdingSummaryLocation,latestCostArray,key,privateKey)==1):
                                delayAfterBigPurchase=30
                            
                            # if (classifications[2]==1 or classifications[1]==1):
                            #     KrakenController.purchaseImmediate(pairs[pair],amounts[2],logFileLocation,maximumHoldingsValue,holdingSummaryLocation,latestCostArray,key,privateKey)
                            # elif (classifications[0]==1):
                            #     KrakenController.purchaseImmediate(pairs[pair],amounts[1],logFileLocation,maximumHoldingsValue,holdingSummaryLocation,latestCostArray,key,privateKey)
                        # if (classifications[2]==1):
                        #     print ("[2] Indicates time to buy (small auto approved purchase)")
                        #     KrakenController.purchaseImmediate(pairs[pair],amounts[0],logFileLocation,maximumHoldingsValue,holdingSummaryLocation,latestCostArray,key,privateKey)
                    else:
                        print("Will not purchase more for the next",delayAfterBigPurchase, "minutes")
                        delayAfterBigPurchase-=1
                else:
                    print ("Above Profitable Sell Price: Will not purchase more.")
                    
                
                # Selling
                if ((classifications[0]==2 and classifications[1]==2 and classifications[2]==2)):
                    KrakenController.sellWithApproval(pairs[pair],logFileLocation,maximumHoldingsValue,holdingSummaryLocation,latestCostArray,key,privateKey,adjustment)

                # Emergency Selling
                if (classifications[4]==2 or classifications[3]==2):
                    print ("Selling if above breakeven ONLY if [3] or [4] are classified as sells...")
                    KrakenController.sellWithApproval(pairs[pair],logFileLocation,maximumHoldingsValue,holdingSummaryLocation,latestCostArray,key,privateKey,breakevenAdjustment)

            minutes=timeControl
            # print ("Waiting Until Next Batch for "+str(minutes)+ " Minutes")
            for i in range(minutes):
                time.sleep(60)
                minutes-=1
                # print ("Waiting for "+str(minutes)+ " Minutes")

    # Message box func
    def print_msg_box(msg, indent=1, width=None, title=None):
        """Print message-box with optional title."""
        lines = msg.split('\n')
        space = " " * indent
        if not width:
            width = max(map(len, lines))
        box = f'╔{"═" * (width + indent * 2)}╗\n'  # upper_border
        if title:
            box += f'║{space}{title:<{width}}{space}║\n'  # title
            box += f'║{space}{"-" * len(title):<{width}}{space}║\n'  # underscore
        box += ''.join([f'║{space}{line:<{width}}{space}║\n' for line in lines])
        box += f'╚{"═" * (width + indent * 2)}╝'  # lower_border
        print(box)

    def purchaseImmediate(pair,amount,logFileLocation,maximumHoldingsValue,holdingSummaryLocation,latest,key,privateKey):
        print ("Automatically Approved Purchase...")
        approximateCost=(amount*latest[len(latest)-1])
        print ("Cost of Purchase:",approximateCost)
        if ((KrakenController.holdingsValue(holdingSummaryLocation)+approximateCost)<maximumHoldingsValue):
            ka.MarketBuy(key,privateKey,amount,pair)
            KrakenController.updateMainLog('BUY',pair,amount,logFileLocation)
            KrakenController.logPurchase(pair,amount,holdingSummaryLocation)
            print ("Bought around: ",str(latest[len(latest)-1]))
            return 1
        else:
            print ("Max Holdings Value")
            return 0

    def purchaseWithApproval(pair,amount,logFileLocation,maximumHoldingsValue,holdingSummaryLocation,latest,key,privateKey):
        print ("Purchase only with Approval...")
        approximateCost=(amount*latest[len(latest)-1])
        print ("Cost of Purchase:",approximateCost)
        if ((KrakenController.holdingsValue(holdingSummaryLocation)+approximateCost)<maximumHoldingsValue):
            if (KrakenController.approvePurchase(pair,holdingSummaryLocation)==1):
                ka.MarketBuy(key,privateKey,amount,pair)
                KrakenController.updateMainLog('BUY',pair,amount,logFileLocation)
                KrakenController.logPurchase(pair,amount,holdingSummaryLocation)
                print ("Bought around: ",str(latest[len(latest)-1]))
            else:
                print ("Purchase Not Approved: Too High to Average Down")
        else:
            print ("Max Holdings Value: Cannot Afford to Purchase More")

    def sellWithApproval(pair,logFileLocation,maximumHoldingsValue,holdingSummaryLocation,latest,key,privateKey,minSellAdjustment):
        print ("Selling With Approval...")
        if (KrakenController.approveSale(pair,minSellAdjustment,holdingSummaryLocation)==1):
            amountToSell=KrakenController.getHoldingAmount(pair,holdingSummaryLocation)
            amountToSell=(round(amountToSell, 2))
            # amountToSell=(round(amountToSell*0.99, 4)) 
            ka.MarketSell(key,privateKey,amountToSell,pair)
            KrakenController.updateMainLog('SELL',pair,amountToSell,logFileLocation)
            KrakenController.logSale(pair,amountToSell,holdingSummaryLocation)
            print ("Sold Around: ",str(latest[len(latest)-1]))
        else:
            print ("Sale Not Approved: Price too low")

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
                if (lastPrice>=cost*0.98):
                    return 0
        return 1
    
    def getAverageCost(pair,holdingSummaryLocation):
        data=hp.holdingCheck(holdingSummaryLocation)
        for x in range(len(data)):
            if(data[x].split(',')[0]==pair):
                cost=float(data[x].split(',')[2])
                return cost
        return 0

    def getHoldingsAmount(pair,holdingSummaryLocation):
        data=hp.holdingCheck(holdingSummaryLocation)
        for x in range(len(data)):
            if(data[x].split(',')[0]==pair):
                cost=float(data[x].split(',')[1])
                return cost
        return 0

    def approveSale(pair,minimumProfit,holdingSummaryLocation):
        entryExists=0
        lastPrice=ka.getCurrentPrice(1,'lastOnly',pair)
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
    
    def getHoldingsList(holdingSummaryLocation):
        data=hp.holdingCheck(holdingSummaryLocation)
        res=[]
        for x in range(len(data)):
            temp=[]
            temp.append(data[x].split(',')[0])
            temp.append(data[x].split(',')[1])
            temp.append(data[x].split(',')[2])
            res.append(temp)
        return res
