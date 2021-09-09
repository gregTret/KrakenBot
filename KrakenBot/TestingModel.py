import warnings
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
import torchvision
from torch.utils.data import DataLoader
import torch.nn.functional as F
from PIL import Image
from os import walk
from .CustomDataset import newDataSet
from .Helper import HelperFunctions as hp
import shutil

class TestingModel:
    def TestModel(modelDirectory,directoryName,specificFolder):
        tensorResults=[]
        # Checking Accuracy Function
        def check_accuracy(loader, model):
            num_correct = 0
            num_samples = 0
            model.eval()
            with torch.no_grad():
                for x, y in loader:
                    x = x.to(device=device)
                    y = y.to(device=device)
                    scores = model(x)
                    _, predictions = scores.max(1)
                    num_correct += (predictions == y).sum()
                    num_samples += predictions.size(0)
                    tensorResults.append(predictions)
                print(
                    f"Got {num_correct} / {num_samples} with accuracy {float(num_correct)/float(num_samples)*100:.2f}"
                )
        # Disabling Warnings
        warnings.simplefilter(action='ignore', category=FutureWarning)
        warnings.simplefilter(action='ignore', category=UserWarning)
        # Loading up Model
        model=torchvision.models.googlenet(pretrained=True)
        model.load_state_dict(torch.load(modelDirectory),strict=False)
        # Model Variables
        model.eval()
        in_channel=3
        num_classes=2
        learning_rate=1e-3
        batch_size=32
        num_epochs=15
        # Loading Data for testing
        dataset= newDataSet(csv_file=directoryName+'classifications.csv',root_dir=directoryName+specificFolder,transform = transforms.ToTensor())
        test_loader=DataLoader(dataset=dataset,batch_size=batch_size,shuffle=False)
        print (test_loader)
        # Setting Device 
        device = torch.device ('cuda' if torch.cuda.is_available() else 'cpu')
        print ("Using:",device)
        model.to(device)
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=learning_rate) 
        check_accuracy(test_loader, model)
        return (tensorResults)

    def ClassifyImage(modelLocation,testLocation,deviceUsedForModel):
        # Disabling Warnings
        warnings.simplefilter(action='ignore', category=FutureWarning)
        warnings.simplefilter(action='ignore', category=UserWarning)
        # Loading In Googlenet Model
        model=torchvision.models.googlenet(pretrained=True)
        # Loading Trained Model
        try:
            model.load_state_dict(torch.load(modelLocation),strict=False)
        except:
            model.load_state_dict(torch.load(modelLocation,map_location=torch.device('cpu')),strict=False)
            pass
        try:
            model.load_state_dict(torch.load(modelLocation),strict=False)
        except:
            model.load_state_dict(torch.load(modelLocation,map_location=torch.device('cpu')),strict=False)
            pass
        # Setting Device 
        model.to(deviceUsedForModel)
        # Setting model to eval mode
        model.eval()
        img = Image.open(testLocation)
        test_transforms = transforms.ToTensor()
        # Converting Image to Tensor
        image_tensor = test_transforms(img).float()
        image_tensor = image_tensor.unsqueeze_(0)
        # Returning Model Output
        output = model(image_tensor)
        index = output.data.cpu().numpy().argmax()
        return (index)

    # def ClassifyImagesInDirectory(modelLocation,directory,deviceUsedForModel):
    #     data=[]
    #     counter=0
    #     sd=next(walk(directory),(None, None, []))[2]
    #     hp.CreateImageFolders(directory)
    #     for x in sd:
    #         if (x[0]=='n'):
    #             shutil.move(directory +'/'+ x, directory+'/nothing/'+x)
    #         elif (x[0]=='b'):
    #             shutil.move(directory +'/'+ x, directory+'/buy/'+x)
    #         elif (x[0]=='s'):
    #             shutil.move(directory +'/'+ x, directory+'/sell/'+x)
    #     hp.CSVBuilderClassification(directory)
    #     quit()
    #     directoryList=[directory+'/nothing/',directory+'/buy/',directory+'/sell/']
    #     for x in directoryList:
    #         sd=next(walk(x),(None, None, []))[2]
    #         for i in sd:
    #             tmp=[]
    #             tmp.append(i)
    #             tmp.append(str(counter))
    #             data.append(tmp)
    #         counter+=1
    #     hp.D2listToCSV(data,directory+"/classifications.csv")