import os
import time
from TestingModel import * 
from KrakenApi import *
import subprocess

# Setting Directories up
directory_path = os.getcwd()
modelLocation=directory_path+'/generatedModels/customModel.pth'
testLocation=directory_path+'/tests/tmp.jpeg'

while (KrakenStatus()==0):
    # Spacing Out Requests
    time.sleep(5)
    # Getting Monero Prices
    latest=XMRUSD(5,'high')
    # Converting list to JPEG
    ListToJPEG(latest,testLocation)
    # Classifying Image based on Model
    if (ClassifyImage(modelLocation, testLocation)==1):
        print ("XMR is Low Purchase at: "+str(latest[len(latest)-1]))
        subprocess.call(["notify-send",'Testing Notifications',"Go Check Kraken out", '-u','critical'])
    else:
        print ("Current Price: "+str(latest[len(latest)-1]))
    # Waiting for 5 minutes
    time.sleep(60*5)
    

