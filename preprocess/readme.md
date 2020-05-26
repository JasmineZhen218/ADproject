# Image preprocessing

The goal of this section is to prepare training dataset for training neural network in the next step. The large pathology images were cropped into small pieces. Pieces and their pixel-wise labelling were saved. 

#### Introduction 

There are two kinds of biomarkers for in AD pathology images:

1) Tau tangle: They are neurofibrillary tangles caused by the detachment of a protein, tau.  Pathology images were stained by 6E10( immune antibody of tau) for tau tangle visualization.

2) Amyloid plaque: They are caused by the deposit of Amyloid-beta on axons of neurons. Pathology images were stained by PHF-1( immune antibody of amyloid) for amyloid plaque visualization.

#### Input

To extract samples from large pathology images, you have to ensure that these 3 files exist:

[1] `Base.tif`   This is the original pathology image

[2] `SampleZone.nii.gz`  Not all the pixels were annotated and this file record which pixels were annotated. Pixels annotated were labeled as 1, otherwise 0. Normally the annotated regions are several squares.

[3] `Biomarker.nii.gz` This file record which pixels were annotated as biomarkers. Pixels annotated as biomarkers were labeled as 1. Pixels that were annotated as non-biomarker or not been annotated were labeled as 0.

### How to run code

To extract samples from annotated pathology images, firstly install the requirements from the `requirements.txt`, then run the script `creat_td.py`. It takes 5 arguments (the 5th is optional)

  [1] number of samples you want to extract from this pathology image
  [2] number of samples having been in the dataset directory where you are going to save extracted samples
  [3] path to annotation directory which contained  `base.tif, SampleZone.nii.gz, Biomarker.nii.gz`
  [4] path to directory you want to save extracted samples
  [5] (optional) height and width of samples you are going to extract, default is (132,132)

An example command to run the file would look like:

```
python creat_td.py 500 0 asset/Annotation asset/Samples (132,132)
```

### Output

The output are a bunch of NDARRAYs named as `1.npy`, `2.npy`, etc.   The number in the name is the unique ID assigned to  each sample. The name format should not be changed as they would be used in the UNET training in the next section. If you must change the name, go to `Dataloader` and make corresponding edition. Each samples is a 132 x 132 x 4 NEARRAY. The first 3 channels contain information from `Base.tif`, the last channel contains information from `Biomarker.nii.gz`

Visualize some examples in https://github.com/JasmineZhen218/ADproject/blob/master/preprocess/visualize%20samples.ipynb



