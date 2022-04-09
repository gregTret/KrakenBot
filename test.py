import KrakenBot 
from KrakenBot import KrakenController as KrakenController
from KrakenBot import KrakenApiRequests as KrakenApiRequests
from KrakenBot import HelperFunctions as HelperFunctions
from KrakenBot import TestingModel as TestingModel
from KrakenBot import TestBuilder as TestBuilder
from KrakenBot import TrainingModel as TrainModel
import os
import json

# Setting Directories up            
directory_path = (KrakenBot.__path__[0])
trainingPath=directory_path+'/generatedData/set/'
modelSaveLocation=directory_path+'/generatedModels/1.5.pth'
testLocation=directory_path+'/tests/tmp.jpeg'
classificationSave=directory_path+'/tests'
logFileLocation=directory_path+'/logs/logs.txt'
holdingSummaryLocation=directory_path+'/logs/holdings.txt'
modelLocation=directory_path+'/generatedModels/1.4.3_b.pth'
massSortingDirectory='E:\gits\Data Sets\MAIN_LARGEST_DATASET\\1.5\\images'
trainingPath='E:\gits\Data Sets\MAIN_LARGEST_DATASET\\1.5\\training\\'
configFile=directory_path+'/logs/configuration.json'

# Loading Configuration File
configuration=(HelperFunctions.readConfigurationFile(configFile))
key= configuration['key']
privateKey= configuration['privateKey']
minSellAdjustment=configuration['minSellAdjustment']
maximumHoldingsValue=configuration['maximumHoldingsValue']
barsToUse=configuration['barsToUse']
timeControl=configuration['timeControl']    
deviceUsedToModel=configuration['deviceUsedToModel'] 
numEpochs=configuration['numEpochs']
amount=[]
pair=[]
for attribute, value in configuration['pairs'].items():
    pair.append(attribute)
    amount.append(value)

# HelperFunctions.SetupDirectories(directory_path)
# HelperFunctions.CSVBuilderClassification('E:\gits\Data Sets\MAIN_LARGEST_DATASET\\1.5\\images')
# TestingModel.ClassifyImages(modelLocation,massSortingDirectory,deviceUsedToModel)
# TrainModel.train(trainingPath,modelSaveLocation, numEpochs)
# HelperFunctions.CSVBuilderClassification(classificationSave)
# KrakenController.tradingBot(key,privateKey,pair,amount,minSellAdjustment,maximumHoldingsValue,barsToUse,timeControl,testLocation,classificationSave,modelLocation,logFileLocation,holdingSummaryLocation,deviceUsedToModel)
# amountsXMR=[0.02, 0.1, 0.1, 0.1, 0.1]
amountsXMR=[0.2, 0.5, 0.75, 1.0, 1.0]
amountsArray=[]
amountsArray.append(amountsXMR)
pairsArray=['DOTUSD']
KrakenController.newTradingBot(amountsArray,key,privateKey,pairsArray,minSellAdjustment,maximumHoldingsValue,timeControl,testLocation,classificationSave,modelLocation,logFileLocation,holdingSummaryLocation,deviceUsedToModel)
