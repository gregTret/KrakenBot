import KrakenBot
from KrakenBot import KrakenController as KrakenController
from KrakenBot import HelperFunctions as HelperFunctions
from KrakenBot import TestingModel as TestingModel
from KrakenBot import TestBuilder
from KrakenBot import TrainingModel as TrainModel
import os

# Kraken API Public and Private Key
key= 'yourpublickey'
privateKey= 'yourprivatekey'

# Crypto[=currency Pair to Buy/Sell and Desired Amount
pair=["XMRUSD","ETHUSD"] 
minSellAdjustment=[1.01,1.01]
amount=[0.1,0.01]

# Risk Level (1= Very High , 5 = High , 15 = Medium, 30 = Low, 60 = Lowest)
barsToUse=60
# Time Between Request Batches
timeControl=10
counter=1530
# Device used to generate models: by default set to cpu
deviceUsedToModel='cpu'
numEpochs=20

# Setting Directories up
directory_path = os.getcwd()+'/KrakenBot'
trainingPath=directory_path+'/generatedData/set/'
modelLocation=directory_path+'/generatedModels/1.1.pth'
modelSaveLocation=directory_path+'/generatedModels/new_model.pth'
testLocation=directory_path+'/tests/tmp.jpeg'
classificationSave=directory_path+'/tests'

# HelperFunctions.SetupDirectories(directory_path)
# TrainModel.train(trainingPath,modelSaveLocation,numEpochs)
# HelperFunctions.CSVBuilderClassification(classificationSave)
KrakenController.evaluationMode(pair,barsToUse,timeControl,testLocation,classificationSave,modelLocation,deviceUsedToModel,counter)
# KrakenController.tradingBot(key,privateKey,pair,amount,minSellAdjustment,barsToUse,timeControl,testLocation,classificationSave,modelLocation,deviceUsedToModel,counter)

