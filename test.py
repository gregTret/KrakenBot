import KrakenBot 
from KrakenBot import KrakenController as KrakenController
from KrakenBot import HelperFunctions as HelperFunctions
from KrakenBot import TestingModel as TestingModel
from KrakenBot import TestBuilder as TestBuilder
from KrakenBot import TrainingModel as TrainModel
import os

# Kraken API Public and Private Key
key= 'yourpublickey'
privateKey= 'yourprivatekey'
pair=["XMRUSD","LTCUSD"] 
minSellAdjustment=[1.01,1.01]
amount=[0.15,0.05]
maximumHoldingsValue=500

# Risk Level (1= Very High , 5 = High , 15 = Medium, 30 = Low, 60 = Lowest)
barsToUse=15
timeControl=5

# Ignore For now will be phased out
counter=3773

# Device used to generate models: by default set to cpu 
deviceUsedToModel='cpu'
numEpochs=30
# Setting Directories up
directory_path = os.getcwd()+'/KrakenBot'
trainingPath=directory_path+'/generatedData/set/'
modelSaveLocation=directory_path+'/generatedModels/new_model.pth'
testLocation=directory_path+'/tests/tmp.jpeg'
classificationSave=directory_path+'/tests'
logFileLocation=directory_path+'/logs/logs.txt'
holdingSummaryLocation=directory_path+'/logs/holdings.txt'
modelLocation=(KrakenBot.__path__[0])+'/generatedModels/1.4.1.pth'
massSortingDirectory='E:\gits\Data Sets\MAIN_LARGEST_DATASET\\1.4\\nextLevel\\backup'

HelperFunctions.SetupDirectories(directory_path)
# HelperFunctions.CSVBuilderClassification('E:\gits\Data Sets\MAIN_LARGEST_DATASET\\1.4\\nextLevel\\1.4.0_sorted')
# TestingModel.ClassifyImages(modelLocation,massSortingDirectory,deviceUsedToModel)
# TrainModel.train(trainingPath,modelSaveLocation,numEpochs)
# HelperFunctions.CSVBuilderClassification(classificationSave)
# KrakenController.evaluationMode(pair,barsToUse,timeControl,testLocation,classificationSave,modelLocation,logFileLocation,holdingSummaryLocation,deviceUsedToModel,counter)
KrakenController.tradingBot(key,privateKey,pair,amount,minSellAdjustment,maximumHoldingsValue,barsToUse,timeControl,testLocation,classificationSave,modelLocation,logFileLocation,holdingSummaryLocation,deviceUsedToModel,counter)

