import os
import time
from TestingModel import * 
from KrakenApi import *
import subprocess

# Setting Directories up
directory_path = os.getcwd()
modelLocation=directory_path+'/generatedModels/customModel1030.pth'
testLocation=directory_path+'/tests/tmp.jpeg'

while (KrakenStatus()==0):
    # Spacing Out Requests
    time.sleep(5)
    # Getting Monero Prices
    latest=XMRUSD(5,'average')
    # Converting list to JPEG
    ListToJPEG(latest,testLocation)
    # Classifying Image bassed on Model
    if (ClassifyImage(modelLocation, testLocation)==1):
        print ("XMR is Low Currently At: "+str(latest[len(latest)-1]))
        try:
            subprocess.call(["notify-send",'Testing Notifications',"Go Check Kraken out", '-u','critical'])
            subprocess.call(['spd-say','BeepBoopJoeBidenWakeupJoeBidenWakeup'])
        except:
            pass
    else:
        print ("Current Price: "+str(latest[len(latest)-1]))
    # Waiting Until Next Request
    minutes=5   
    print ("Waiting for "+str(minutes)+ " Minutes")
    for i in range(minutes):
        time.sleep(60)
        minutes-=1
        print ("Waiting for "+str(minutes)+ " Minutes")


