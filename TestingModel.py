import warnings
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
import torchvision
from torch.utils.data import DataLoader
import torch.nn.functional as F
from CustomDataset import newDataSet

def TestModel(modelDirectory,directoryName):
    warnings.simplefilter(action='ignore', category=FutureWarning)
    warnings.simplefilter(action='ignore', category=UserWarning)

    model=torchvision.models.googlenet(pretrained=True)
    
    model.load_state_dict(torch.load(modelDirectory),strict=False)

    model.eval()
    in_channel=3
    num_classes=2
    learning_rate=1e-3
    batch_size=32
    num_epochs=15

    dataset= newDataSet(csv_file=directoryName+'classifications.csv',root_dir=directoryName+'images',transform = transforms.ToTensor())
    test_loader=DataLoader(dataset=dataset,batch_size=batch_size,shuffle=True)

    device = torch.device ('cuda' if torch.cuda.is_available() else 'cpu')
    # print ("Using:",device)
    model.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    # Check accuracy on training to see how good our model is
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
            print(
                f"Got {num_correct} / {num_samples} with accuracy {float(num_correct)/float(num_samples)*100:.2f}"
            )  
    check_accuracy(test_loader, model)
