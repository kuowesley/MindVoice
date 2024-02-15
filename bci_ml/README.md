# BCI Project


## Data Preprocessing (Matlab code)

You can download it from this Google Drive link: [https://drive.google.com/drive/folders/1ykR-mn4d4KfFeeNrfR6UdtebsNRY8PU2?usp=sharing]. 
Please download the data and place it in your data_path at "./data."

# Getting Started
  * You can run the code on your Colab or Kaggle (If your model node need GPU)
    * [1.BCI Data Description](https://colab.research.google.com/drive/1gwIGFoSsRLu9-X3Z79xrPMKiqqE_XeMu#scrollTo=366c60d7)
    * [2.BCI EEG classification](https://colab.research.google.com/drive/1E4kb9iRZHc251SXFANzdpfLBfWzw9L2G)
  * To run locally, follow the steps below:
    * Install `poetry` package manager: [https://python-poetry.org/docs/#installation]
    * Run `poetry install` to install the dependencies
    * Run `poetry run python bci_ml.py --n_epoch 30` to run the code. You should be able to see the below output:
      ```
      CUDA can use
      GPU device: cuda:0
      GPU type:  (Your GPU device name)
      Loading data from  data/
      Training data with  30  epochs
      Epoch 1/30, Loss: 1.5879701375961304
      Epoch 2/30, Loss: 1.6449092626571655
      Epoch 3/30, Loss: 1.582672119140625
      Epoch 4/30, Loss: 1.4842877388000488
      Epoch 5/30, Loss: 1.282340168952942
      Epoch 6/30, Loss: 1.3895037174224854
      Epoch 7/30, Loss: 1.1238073110580444
      Epoch 8/30, Loss: 0.9368878602981567
      Epoch 9/30, Loss: 0.7418971061706543
      Epoch 10/30, Loss: 0.6703296303749084
      Epoch 11/30, Loss: 0.5117834806442261
      Epoch 12/30, Loss: 0.5235801339149475
      Epoch 13/30, Loss: 0.5602546334266663
      Epoch 14/30, Loss: 0.3912844657897949
      Epoch 15/30, Loss: 0.31669485569000244
      Epoch 16/30, Loss: 0.3011781573295593
      Epoch 17/30, Loss: 0.30865973234176636
      Epoch 18/30, Loss: 0.40947026014328003
      Epoch 19/30, Loss: 0.18676835298538208
      Epoch 20/30, Loss: 0.37194177508354187
      Epoch 21/30, Loss: 0.342347115278244
      Epoch 22/30, Loss: 0.22979319095611572
      Epoch 23/30, Loss: 0.21958930790424347
      Epoch 24/30, Loss: 0.12275101989507675
      Epoch 25/30, Loss: 0.18813563883304596
      Epoch 26/30, Loss: 0.22806254029273987
      Epoch 27/30, Loss: 0.15258032083511353
      Epoch 28/30, Loss: 0.33962735533714294
      Epoch 29/30, Loss: 0.13499870896339417
      Epoch 30/30, Loss: 0.2773832082748413
      Test Accuracy: 48.30%
      ```
    

# Other EEG featuers extraction methods
- [Matlab packages](#Matlab packages)

## Method

* Classification (Machine learning methods, Scikit-learn[https://scikit-learn.org/stable/])
* Classification (Simple Autoencoder model)

## Data introduction & papers
[2020 BCI competition](https://www.frontiersin.org/articles/10.3389/fnhum.2022.898300/full):  – raw data downloaded and tried D2: data set C(Imagined speech) 


## Model Performance:

Name | Epochs | ACC | Precision | Recall | 
---  |:---------:|:---------:|:---------:|:---------:
Transformer | 500 | Best run:54.69% | - | - | -
DNN | 300 | 53.81% | - | - | -
Classification | - |  ~40% for subject, ~ 35% for cross subject | - | - | -
Confomer | - |  - | - | - | -
RNN | - | ~25% for cross subject  | - | - | -


## References:
- [2020 International brain–computer interface competition: A review](https://www.frontiersin.org/articles/10.3389/fnhum.2022.898300/full)