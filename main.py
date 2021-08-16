import os
from TestBuilder import BuildTest
from TestBuilder import BuildTest
from TrainingModel import TrainModel
from TestingModel import TestModel
from Setup import SetupDirectories

numberOfEpochs=10
directory_path = os.getcwd()
mainDataDirectory=directory_path+'/data/'
testSaveDirectory=directory_path+'/generatedData/'
modelSaveLocation=directory_path+'/generatedModels/model.pth'
extraTestLocation=directory_path+'/tests/'

#First Time Directory Setup
if (SetupDirectories(directory_path)):
    # Building Tests
    BuildTest(mainDataDirectory,testSaveDirectory)
    # Training Models
    TrainModel(testSaveDirectory+'set/',modelSaveLocation,numberOfEpochs)
    # Testing Models (Optional)
    # TestModel(modelSaveLocation,extraTestLocation)
else:
    print ("Completed first time setup. Please add some data to the Data folder to generate models and run again")

    
