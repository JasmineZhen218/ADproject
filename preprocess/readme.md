# Image preprocessing

The goal of this section is to prepare training dataset for training neural network in the next step. The large pathology images were cropped into small pieces. Pieces and their pixel-wise labelling were saved. 

#### Introduction 

There are two kinds of biomarkers for in AD pathology images:

1) Tau tangle: They are neurofibrillary tangles caused by the detachment of a protein, tau.  Pathology images were stained by 6E10( immuno antibody of tau) for tau tangle visualization.

2) Amyloid plaque: They are caused by the deposit of Amyloid-beta on axons of neurons. Pathology images were stained by PHF-1( immuno antibody of amyloid) for amyloid plaque visualization.

<img src="asset/example_tau.png" style="zoom:50%;" />             <img src="asset/example_amyloid.png" style="zoom:50%;" />

#### Pre-request/input

To extract samples from large pathology images, you have to ensure these 3 files exsit:

1) `Base.tif`   This is the original pathology image

2) `SampleZone.nii.gz`  Not all the pixels were annotated and this file record which pixels were annotated. Pixels annotated were labeled as 1, otherwise 0. Normally the annotated regions are several squares.

3) `Biomarker.nii.gz` This file record which pixels were annotated as biomarkers. Pixels annotated as biomarkers were labeled as 1. Pixels that were annotated as non-biomarker or not been annotated were labeld as 0.

Location of annotated Tau-pathology images: 

Location of annotated Amyloid-pathology images: 

### How to run code

1) First, use pip to install the requirements from the `requirements.txt`

2) Navigate to the directory which contains [base.tif, SampleZone.nii.gz, Biomarker.nii.gz] 

3) Run the script `creat_td.py`. It takes 4 arguments:

* [required] number of samples you want to extract from this pathology image
* [required] path to save extracted samples
* [required] number of samples having been in the path you are going to save your samples
* [optional] height and width of samples you are going to extract, default is (132,132)

An example command to run the file would look like:

```
python creat_td.py 500 cis/home/zwang/Documents/ADproject/DatasetUnet/Amyloid/Train 0
```

> This command will extract 500 samples from (the actual number of samples extracted may be slightly less than 500) the pathology image and save them into `cis/home/zwang/Documents/ADproject/DatasetUnet/Amyloid/train`. No samples have been saved in this location before.

### Output

* Sample format

The annotated regions would firstly been located using `SampleZone.nii.gz`. Within each annotated region, a bunch of 132 x 132 (if you do not specify the height and width) pieces would be cropped from both `Base.tif` and `Biomarker.nii.gz`. The extracted sample is a  ndarray array of shape (132,132,4). The first 3 channels contain information from `Base.tif`, the last channel contains information from `Biomarker.nii.gz`

There are 5 examples in `/sample`. You could use `show_sample.inpy` to visualize them.

* Location of extracted samples

Location of tau-samples:

Location of amyloid-samples:





