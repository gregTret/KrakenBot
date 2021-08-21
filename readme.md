## Kraken Cryptocurrency Trading with Pytorch
>Built with and tested on Python 3.8 
<h3> Essential Setup Instructions </h3>

1. Install required Packages. 
Checkout https://pytorch.org/get-started/locally/ for the best Torch installation for your machine. 
Enabling Cuda (GPU) as your device is strongly recommended as it will make testing and training much more efficient. 

2) Run main.py for first time setup

<h3> Kraken Setup </h3>

1. Update your private and public keys inside of KrakenMain.py.

2. Configure the variable lists at the top of KrakenMain.py to reflect your own objectives and risk tolerence.

3. Run KrakenMain.py and enjoy!

<h3> Build Your Own Model Instructions </h3>

1. Place Organized Data into the GeneratedData folder.

2. Call the "TrainModel" function from main.py. Your model is saved by default in "./generatedModels/model.pth".

<h3> Build Your Own Dataset Instructions </h3>

1.  Add file(s) to the "data" folder with your desired testing data. Run the "BuildTest" function inside of main.py to generate testing sets. These testing sets can be used to train models.

2. Unfortunately, this is not enough to generate good dataset. The generation of good datasets is a mixture of manual and automatic classification, and is a process that is still undergoing improvements. 


Required Python Packages


>numpy<br>
torch<br>
scikit-image <br>
pandas<br>
matplotlib <br>
pillow <br>
requests





<h3>Linux Package Installation: </h3>

```bash
pip3 install numpy

pip3 install torch torchvision torchaudio

pip3 install scikit-image

pip3 install pandas

pip3 install matplotlib

pip3 install pillow

pip3 install requests
```
<h3>Windows Package Installation: </h3>

```bash
pip3 install numpy

pip3 install torch==1.9.0+cu102 torchvision==0.10.0+cu102 torchaudio===0.9.0 -f https://download.pytorch.org/whl/torch_stable.html

pip3 install scikit-image

pip3 install pandas

pip3 install matplotlib

pip3 install pillow

pip3 install requests
```