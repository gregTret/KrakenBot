import os
from TestBuilder import BuildTest
from TestBuilder import BuildTest
from TrainingModel import TrainModel
from TestingModel import TestModel

directory_path = os.getcwd()
mainDataDirectory=directory_path+'./data/'
testSaveDirectory=directory_path+'./generatedData/'
modelSaveLocation=directory_path+'./generatedModels/model.pth'
extraTestLocation=directory_path+'./tests/'

# Building Tests
BuildTest(mainDataDirectory,testSaveDirectory)
# Training Models
TrainModel(testSaveDirectory+'set/',modelSaveLocation)
# Testing Models
TestModel(modelSaveLocation,extraTestLocation)


    