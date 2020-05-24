# Image preprocessing

The goal of this section is to prepare training dataset for training neural network in the next step. The large pathology images were cropped into small pieces. Pieces and their pixel-wise labelling were saved. 

#### Introduction 

There are two kinds of biomarkers for in AD pathology images:

1) Tau tangle: They are neurofibrillary tangles caused by the detachment of a protein, tau.  Pathology images were stained by 6E10( immune antibody of tau) for tau tangle visualization.

2) Amyloid plaque: They are caused by the deposit of Amyloid-beta on axons of neurons. Pathology images were stained by PHF-1( immune antibody of amyloid) for amyloid plaque visualization.

#### Input

To extract samples from large pathology images, you have to ensure these 3 files exist:

1) `Base.tif`   This is the original pathology image

2) `SampleZone.nii.gz`  Not all the pixels were annotated and this file record which pixels were annotated. Pixels annotated were labeled as 1, otherwise 0. Normally the annotated regions are several squares.

3) `Biomarker.nii.gz` This file record which pixels were annotated as biomarkers. Pixels annotated as biomarkers were labeled as 1. Pixels that were annotated as non-biomarker or not been annotated were labeled as 0.

* Location of annotated Tau-pathology images: `cis/home/zwang/Documents/ADproject/Annotation/Tau`

* Location of annotated Amyloid-pathology images: `cis/home/zwang/Documents/ADproject/Annotation/Amyloid`

### How to run code

First, use pip to install the requirements from the `requirements.txt`
Ensure you have `base.tif, SampleZone.nii.gz, Biomarker.nii.gz`

Run the script `creat_td.py`. It takes 5 arguments:

  1) number of samples you want to extract from this pathology image
  2) number of samples having been in the dataset directory where you are going to save extracted samples
  3) path to annotation directory which contained  `base.tif, SampleZone.nii.gz, Biomarker.nii.gz`
  4) path to directory you want to save extracted samples
  5) (optional) height and width of samples you are going to extract, default is (132,132)

An example command to run the file would look like:

```
python creat_td.py 500 0 cis/home/zwang/Documents/ADproject/Annotation/Amyloid/1
cis/home/zwang/Documents/ADproject/DatasetUnet/Amyloid/Train 
```

> You are going to extract 500 samples from annotated images in cis/home/zwang/Documents/ADproject/Annotation/Amyloid/1 and save them into cis/home/zwang/Documents/ADproject/DatasetUnet/Amyloid/Train . There are no samples in cis/home/zwang/Documents/ADproject/DatasetUnet/Amyloid/Train before running this script.

### Output

* Sample format

The annotated regions would firstly been located using `SampleZone.nii.gz`. Within each annotated region, a bunch of 132 x 132 (if you do not specify the height and width) pieces would be cropped from both `Base.tif` and `Biomarker.nii.gz`. The extracted sample is a  ndarray array of shape (132,132,4). The first 3 channels contain information from `Base.tif`, the last channel contains information from `Biomarker.nii.gz`

There are 5 examples in `/sample`. You could use `show_sample.inpy` to visualize them.

* Location of extracted samples

Location of tau-samples: `cis/home/zwang/Documents/ADproject/DatasetUnet/Tau`

Location of amyloid-samples: `cis/home/zwang/Documents/ADproject/DatasetUnet/Amyloid`





