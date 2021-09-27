from matplotlib.pyplot import bar
import requests
import json
from flask import Flask, jsonify,request
from flask.helpers import make_response
import KrakenBot 
from KrakenBot import KrakenController as KrakenController
from KrakenBot import KrakenApiRequests as KrakenRequests
from KrakenBot import HelperFunctions as HelperFunctions
from KrakenBot import TestingModel as TestingModel
import warnings
import torch
import torchvision.transforms as transforms
import torchvision
from PIL import Image
from os import walk
import time
import shutil

# Disabling Warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

directory_path = (KrakenBot.__path__[0])
trainingPath=directory_path+'/generatedData/set/'
modelSaveLocation=directory_path+'/generatedModels/1.4.3.pth'
testLocation=directory_path+'/tests/tmp.jpeg'
classificationSave=directory_path+'/tests'
logFileLocation=directory_path+'/logs/logs.txt'
holdingSummaryLocation=directory_path+'/logs/holdings.txt'
modelLocation=directory_path+'/generatedModels/1.4.3_b.pth'
trainingPath='E:\gits\Data Sets\MAIN_LARGEST_DATASET\\1.4.3\\3\\'
configFile=directory_path+'/logs/configuration.json'

# Setting Global vars
key=""
privateKey=""
minSellAdjustment=0
maximumHoldingsValue=0
barsToUse=0
timeControl=0
deviceUsedToModel=''
numEpochs=0
amount=[]
pair=[]

# Loading Global Configuration File
def updateConfigurationVariables():
    global key
    global privateKey
    global minSellAdjustment
    global maximumHoldingsValue
    global barsToUse
    global timeControl
    global deviceUsedToModel
    global numEpochs
    global amount
    global pair
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

updateConfigurationVariables()

# Loading in Model Once for faster Classifications 
# Loading In Googlenet Model
model=torchvision.models.googlenet(pretrained=True)
# Loading Trained Model
try:
    model.load_state_dict(torch.load(modelLocation),strict=False)
except:
    model.load_state_dict(torch.load(modelLocation,map_location=torch.device('cpu')),strict=False)
pass
# Setting Device 
model.to(deviceUsedToModel)
# Setting model to eval mode
model.eval()

# API Specific Image Classification Function (For Faster Classifications)
def ClassifyImageAPI(modelLocation,testLocation,deviceUsedToModel):
    img = Image.open(testLocation)
    test_transforms = transforms.ToTensor()
    # Converting Image to Tensor
    image_tensor = test_transforms(img).float()
    image_tensor = image_tensor.unsqueeze_(0)
    # Returning Model Output
    output = model(image_tensor)
    index = output.data.cpu().numpy().argmax()
    return (index)

# Classify Once (API Specific)
def singleCycleAPI(key,privateKey,pair,amount,minSellAdjustment,maximumHoldingsValue,barsToUse,testLocation,classificationSave,modelLocation,logFileLocation,holdingSummaryLocation,deviceUsedToModel):
        HelperFunctions.CreateImageFolders(classificationSave)
        returnResult=[]
        if (KrakenRequests.KrakenStatus()==0):
            for x in range (len(pair)):
                latest=KrakenRequests.getCurrentPrice(barsToUse, 'average', pair[x])
                HelperFunctions.ListToJPEG(latest,testLocation)
                classification=ClassifyImageAPI(modelLocation, testLocation,deviceUsedToModel)
                if (classification==1):
                    shutil.move(testLocation, classificationSave+'/buy/' +str(int(1000*time.time()))+pair[x]+'.jpeg')
                    if (KrakenController.holdingsValue(holdingSummaryLocation)<maximumHoldingsValue):
                        if (KrakenController.approvePurchase(pair[x],holdingSummaryLocation)==1):
                            KrakenRequests.MarketBuy(key,privateKey,amount[x],pair[x])
                            KrakenController.updateMainLog('BUY',pair[x],amount[x],logFileLocation)
                            KrakenController.logPurchase(pair[x],amount[x],holdingSummaryLocation)
                            priceApprox=float(latest[len(latest)-1])*minSellAdjustment[x]
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
                    if (KrakenController.approveSale(pair[x],minSellAdjustment,holdingSummaryLocation)==1):
                        KrakenRequests.MarketSell(key,privateKey,amountToSell,pair[x])
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

# Initializing App
app = Flask(__name__)

# Pinging Kraken
@app.route('/status', methods=['GET'])
def ping():
    response=KrakenRequests.KrakenStatus()
    if (response==0):
        return make_response(jsonify({'Status':"Online"}), 200)
    else:
        return make_response(jsonify({'Status':"Error"}), 404)

@app.route('/', methods=['GET'])
def mainPage():
    return make_response(jsonify({'Message':'Landing Page for Kraken Bot (Python API)'}), 200)

@app.route('/holdings', methods=['GET'])
def gettingHoldings():  
    res={}
    holdings=KrakenController.getHoldingsList(holdingSummaryLocation)
    for x in holdings:
        row={}
        row['Amount']=(x[1])
        row['Price']=(x[2])
        res[x[0]]=row
    return make_response(jsonify({'holdings':res}), 200)

@app.route('/action', methods=['GET'])
def runOnce():
    res={}
    actions=singleCycleAPI(key,privateKey,pair,amount,minSellAdjustment,maximumHoldingsValue,barsToUse,testLocation,classificationSave,modelLocation,logFileLocation,holdingSummaryLocation,deviceUsedToModel)
    for x in actions:
        row={}
        row['Action']=(x[0])
        row['Price']=(x[2])
        row['Amount']=(x[3])
        row['Classification']=(x[4])
        res[x[1]]=row
    return make_response(jsonify({'actions':res}), 200)

@app.route('/configuration', methods=['GET'])
def getConfiguration():
    configuration=(HelperFunctions.readConfigurationFile(configFile))
    return json.dumps(configuration,indent=4)

@app.route('/configuration', methods=['POST'])
def addRecipe():
    try:
        requestData = json.loads(request.data)
    except:
        return make_response(jsonify({'error':'Error in JSON'}), 400)
    with open(configFile, 'w') as f:
        json.dump(requestData, f, indent=4)
    try:
        updateConfigurationVariables()
    except:
        return make_response(jsonify({'error':'Error in Configuration file, may need to manually reset'}), 400)
    return make_response(jsonify({'Status':"Success"}), 200)

app.run(port=3000)