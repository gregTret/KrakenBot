## Kraken Cryptocurrency Trading with Pytorch
>Built with and tested on Python 3.9 <br>
>Using CUDA 11.1

## Releases
The project can be cloned directly from the Github page, or from these releases (newer releases are less prone to errors).<br>
https://github.com/gregTret/KrakenBot/releases/tag/1.3


<h3> Package Installation </h3>

1. Install required Packages. 
Checkout https://pytorch.org/get-started/locally/ for the best Torch installation for your machine. 
Enabling Cuda (GPU) as your device is strongly recommended.

```bash
pip3 install numpy

pip3 install torch==1.9.0+cu111 torchvision==0.10.0+cu111 torchaudio==0.9.0 -f https://download.pytorch.org/whl/torch_stable.html

pip3 install scikit-image

pip3 install pandas

pip3 install matplotlib

pip3 install pillow

pip3 install requests
```


## Setup

1. The UI is in active development, but for now variables must be updated inside of the configuration.json file inside of the log folder.

2. Variables that need Updating: <br>
```
{
    "key": "",
    "privateKey": "",
    "deviceUsedToModel": "cpu",
    "numEpochs": 30,
    "minSellAdjustment": 1.01,
    "maximumHoldingsValue": 500,
    "barsToUse": 15,
    "timeControl": 3,
    "pairs": {
        "XMRUSD": 0.25,
        "ETHUSD": 0.01
    }
}


# Your Kraken Public Key (string)
key= 'yourpublickey' 

# Your Kraken Private Key (string)
privateKey= 'yourprivatekey' 

# The maximum amount to permit the value of your holdings to be. (float)
maximumHoldingsValue=500


```


2. Run test.py, call KrakenController.evaluationMode() to evaluate the model or KrakenController.tradingBot() to enable live trading. 

<br>

## Optional Setup

<h3> Build Your Own Dataset and Model Instructions </h3>

1.  Add file(s) to the "data" folder with your desired testing data. Run TestBuilder.BuildTest() to generate the image files.

2. Once the image files are generated you can classify them using the TestingModel.ClassifyImages() function, and store the results inside of one of thee folders within the './tests/' directory. The function also creates a 'classifications.csv' file which holds the classification information for each image. You can review these manually to verify the model.

3. Once the classifications are verified, you can move all the images from the three folders into a single 'images' folder and move it along with the 'classifications.csv' folder into the 'generatedData' folder. 

4. Running the TrainingModel.train() function with reference to the newly generated data folder will create a new custom model. This model will by default be saved under '/generatedModels/new_model.pth'.



