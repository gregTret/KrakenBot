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
pair=["XMRUSD","ETHUSD"]
minSellAdjustment=[1.01,1.01]
amount=[0.25,0.01]  
maximumHoldingsValue=500


# Risk Level (1= Very High , 5 = High , 15 = Medium, 30 = Low, 60 = Lowest)
barsToUse=5
timeControl=2 

# Device used to generate models: by default set to cpu 
deviceUsedToModel='cpu'
numEpochs=30
# Setting Directories up
directory_path = os.getcwd()+'/KrakenBot'
trainingPath=directory_path+'/generatedData/set/'
modelSaveLocation=directory_path+'/generatedModels/1.4.3.pth'
testLocation=directory_path+'/tests/tmp.jpeg'
classificationSave=directory_path+'/tests'
logFileLocation=directory_path+'/logs/logs.txt'
holdingSummaryLocation=directory_path+'/logs/holdings.txt'
modelLocation=(KrakenBot.__path__[0])+'/generatedModels/1.4.3_b.pth'

massSortingDirectory='E:\gits\Data Sets\MAIN_LARGEST_DATASET\\1.4.3\\sorting\\'
trainingPath='E:\gits\Data Sets\MAIN_LARGEST_DATASET\\1.4.3\\3\\'

HelperFunctions.SetupDirectories(directory_path)
# HelperFunctions.CSVBuilderClassification('E:\gits\Data Sets\MAIN_LARGEST_DATASET\\1.4.3\\3')
# TestingModel.ClassifyImages(modelLocation,massSortingDirectory,deviceUsedToModel)
# TrainModel.train(trainingPath,modelSaveLocation, numEpochs)
# HelperFunctions.CSVBuilderClassification(classificationSave)
# KrakenController.evaluationMode(pair,barsToUse,timeControl,testLocation,classificationSave,modelLocation,logFileLocation,holdingSummaryLocation,deviceUsedToModel)
KrakenController.tradingBot(key,privateKey,pair,amount,minSellAdjustment,maximumHoldingsValue,barsToUse,timeControl,testLocation,classificationSave,modelLocation,logFileLocation,holdingSummaryLocation,deviceUsedToModel)

