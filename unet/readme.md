# Semantic segmentation using U-net

The goal of this section is to train U-net models using annotated images and then apply pretrained models to unlabeled images to form a probability map. The value of each pixel on that map represents the probability of being a biomarker or not.

U-net is convolutional network architecture for fast and precise segmentation of image. For more information, see https://lmb.informatik.uni-freiburg.de/people/ronneber/u-net/. 

### Train/test a U-net Model

#### Train a UNET model

##### Input

* Location of annotated Tau-pathology images: `/cis/home/zwang/Documents/ADproject/Annotation/Tau`

* Location of annotated Amyloid-pathology images: `/cis/home/zwang/Documents/ADproject/Annotation/Amyloid`

##### How to run the codes

To train a UNET model from scratch or based on pretrained model, run the script `train.py`. It takes 5 arguments, the last one is only needed if you want to trained based on pretrained model

​	[1] Trainset_path: path to training dataset
​	[2] batch_size: training batch size, recommend 16
​	[3] nepochs: number of epochs, recommend 3 as the dataset is quite big
​	[4] model_save_path: path to save the trained model
​	[5] (optional) model_load_path: path to pretrained model if you don't want to train from scratch

Example to run `train.py` from scratch:

```
python train.py /cis/home/zwang/Documents/ADproject/DatasetUnet/Tau/Train 16 3  /cis/home/zwang/Documents/ADproject/DatasetUnet/UnetModels/unet_tau.pth 
```

Example to run `train.py` on the basis of a pre-trained model

```
python train.py /cis/home/zwang/Documents/ADproject/DatasetUnet/Tau/Train 16 3  /cis/home/zwang/Documents/ADproject/UnetModels/unet_tau_version2.pth /cis/home/zwang/Documents/ADproject/UnetModels/unet_tau.pth
```

##### Output

The up-to-date model will be saved in the path you specified 



#### Test a UNET model

##### Input

​	[1] Samples to test: There should be a bunch of 132 x 132 x 4 samples described in [Preprocess section](https://github.com/JasmineZhen218/ADproject/blob/master/preprocess/readme.md)

​	[2] A pre-trained UNET model

##### How to run the codes

To test a UNET model , run the script `test.py`. It takes 2 arguments：

​	[1] path to directory containing a bunch of samples 
​	[2] path to pre-trained UNET model you want to test

Example to run `test.py`:

```
python train.py cis/home/zwang/Documents/ADproject/DatasetUnet/Tau/Test  cis/home/zwang/Documents/ADproject/DatasetUnet/UnetModels/unet_tau.pth 
```

> It will test the  UNET model `/cis/home/zwang/Documents/ADproject/DatasetUnet/UnetModels/unet_tau.pth`  on samples in `/cis/home/zwang/Documents/ADproject/DatasetUnet/Tau/Test`  

##### Output

Nothing will be saved after running `test.py`. But you will see AUC, confusion matrix, accuracy on terminal



### Apply trained model to unlabeled pathology image

##### Input

​	[1] Unlabeled pathology image: It should be a 3-channel `tif` image

​	[2] pre-trained model: It should be a PyTorch model 

##### How to run the code

To apply a model on a labeled pathology image, run the script `apply.py`. It takes 3 arguments:

​	[1] path to unlabeled pathology image

​	[2] path to pre-trained model

​	[3] path to save the probability map

An example to run `apply.py`:

```
python apply.py  asset/Base_amyloid.tif asset/unet_amyloid.pth asset/Prob_map.npy
```

##### Output demo

​	[1] Probability map: It should be a 1-channel NDARRAY file. The value of each pixel represents the probability of being a biomarker here.

See the comparison of original base images and probability map in https://github.com/JasmineZhen218/ADproject/blob/master/unet/Visualize%20pathology%20image%20and%20probability%20map.ipynb











