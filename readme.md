## Pytorch Binary Image Classification
>Built with and tested on Python 3.8 


<h3> Setup Instructions </h3>

1) Install required Packages
2) Run main.py for first time setup
3) Add file(s) to the /data folder with your desired testing data. Run main.py to generate testing sets, run training and to generate a model.
4) (Optional) The Generated data can be moved into the /tests directory and new data sets and models can be generated and tested against it. 

Required Python Packages


>numpy<br>
torch<br>
scikit-image <br>
pandas<br>
matplotlib

Checkout :
https://pytorch.org/get-started/locally/ for the best Torch installation for your machine.

Enabling Cuda (GPU) as your device is strongly recommended as it will make testing and training far more time efficient. 




>For Linux Package Installation: 
```bash
pip3 install numpy

pip3 install torch torchvision torchaudio

pip3 install scikit-image

pip3 install pandas

pip3 install matplotlib
```
>For Windows Package Installation:
```bash
pip3 install numpy

pip3 install torch==1.9.0+cu102 torchvision==0.10.0+cu102 torchaudio===0.9.0 -f https://download.pytorch.org/whl/torch_stable.html

pip3 install scikit-image

pip3 install pandas

pip3 install matplotlib
```