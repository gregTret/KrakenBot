from KrakenBot.Helper import HelperFunctions
from KrakenBot import KrakenController as KrakenController
from KrakenBot import HelperFunctions as HelperFunctions
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
counter=1519
# Device used to generate models: by default set to cpu
deviceUsedToModel='cpu'

# Setting Directories up
directory_path = os.getcwd()+'/KrakenBot'
modelLocation=directory_path+'/generatedModels/overtrained_model.pth'
testLocation=directory_path+'/tests/tmp.jpeg'
classificationSave=directory_path+'/tests'

HelperFunctions.SetupDirectories(directory_path)
KrakenController.evaluationMode(pair,barsToUse,timeControl,testLocation,classificationSave,modelLocation,deviceUsedToModel,counter)
KrakenController.tradingBot(key,privateKey,pair,amount,minSellAdjustment,barsToUse,timeControl,testLocation,classificationSave,modelLocation,deviceUsedToModel,counter)

