# Semantic segmentation using U-net

The goal of this section is to train U-net models using annotated images and then apply pretrained models to unlabeled images to form a probability map. The value of each pixel on that map represents the probability of being a biomarker or not.

U-net is convolutional network architecture for fast and precise segmentation of image. For more information, see https://lmb.informatik.uni-freiburg.de/people/ronneber/u-net/. 

### Train/test a U-net Model

##### Input

Location of tau tangle samples (CIS file system):

 `cis/home/zwang/Documents/ADproject/DatasetUnet/Tau`

Location of amyloid plaque samples (CIS file system): `cis/home/zwang/Documents/ADproject/DatasetUnet/Amyloid`

##### How to run the codes

To train a unet model from scratch or based on pretrained model, run the script `train.py`. It takes 5 arguments, the last one is only needed if you want to trained based on pretrained model

1) Trainset_path: path to training dataset
2) batch_size: training batch size, recommend 16
3) nepochs: number of epochs, recommend 3 as the dataset is quite big
4) model_save_path: path to save the trained model
5) (optional) model_load_path: path to pretrained model if you don't want to train from scratch

Example to run `train.py`:

```
python train.py cis/home/zwang/Documents/ADproject/DatasetUnet/Tau/Train 16 3  cis/home/zwang/Documents/ADproject/DatasetUnet/UnetModels 
```

> It will train a unet model aming to detect Tau tangle based on samples in cis/home/zwang/Documents/ADproject/DatasetUnet/Tau/Train from scratch. Training batch size is 16 and number of epochs is 3

The up-to-date model will be saved after running `train.py`



To test a unet model , run the script `test.py`. It takes 2 arguments

1) Testset_path: path to dataset you want to test on
2) input_path: path to unet model you want to test

Example to run `test.py`:

```
python train.py cis/home/zwang/Documents/ADproject/DatasetUnet/Tau/Test  cis/home/zwang/Documents/ADproject/DatasetUnet/UnetModels/unet_tau.pth 
```

> It will test the  unet model cis/home/zwang/Documents/ADproject/DatasetUnet/UnetModels/unet_tau.pth  on samples in cis/home/zwang/Documents/ADproject/DatasetUnet/Tau/Test  

Nothing will be saved after running `test.py`. But you will see AUC, confusion matrix, accuracy on standard output.

##### Output

Location of pretrained models(in GitHub): https://github.com/JasmineZhen218/ADproject/blob/master/unet/asset

Location of pretrained models(in CIS file system): `cis/home/zwang/Documents/ADproject/DatasetUnet/UnetModels`

### Apply trained model to unlabeled pathology image

##### Input

1) Unlabeled pathology image

2) model

##### How to run the code

To apply a model on a labeled pathology image, run the script `apply.py`. It takes 3 arguments:

1) path to unlabeled pathology image

2) path to model

3) path to save the probability map

An example to run `apply.py`:

```
python apply.py cis/home/
```











