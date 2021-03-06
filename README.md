# AD pathology analysis

This is a repository for processing and analyzing pathology images of Alzheimer disease(AD) patients. It consists of 4 sections: 1) Image preprocessing; 2) Semantic segmentation using UNET; 3) Feature extraction; 4) Multiresolution analysis.

### Image preprocessing

The goal of this section is to prepare training dataset for training neural network in the next step. The large pathology images were cropped into small pieces. Pieces and their pixel-wise labelling were saved in a 132 x 132 x 4 ndarray.

Details of codes, data and demo: https://github.com/JasmineZhen218/ADproject/blob/master/preprocess/readme.md

### Semantic segmentation using UNET

The goal of this section is to train UNET models using annotated images and then apply pretrained models to unlabeled images to form a probability map. The value of each pixel on that map represents the probability of being a biomarker or not.

* STEP1: Train UNET models and evaluate performance
* STEP2: Apply satisfactory UNET models to unlabeled images to form probability map

Detailed of codes , pretrained  models and demo: https://github.com/JasmineZhen218/ADproject/blob/master/unet/readme.md

### Feature extraction

The goal of this section is to every biomarkers from probability map  and describe their size, location, orientation and roundness.

* STEP1: Use watershed to get the clear contour of each biomarker from probability map
* STEP2: Assign an ID and describe each biomarker and save the [ID: features] in to `description.csv` files 

Detailed of codes, results and demo: https://github.com/JasmineZhen218/ADproject/blob/master/FeatureExtraction/readme.md

### Multiresolution analysis

The goal of this section is to reconstruct feature map from the `description.csv` files and conduct multiresolution analysis

* STEP1: Reconstruct feature map by "filling" each biomarker with its corresponding features. There would be one feature map for each feature, such as `size_map`, `orientation_map`.
* STEP2:  Calculate local average and local standard deviation on these maps using Gaussian smoothing with various `sigma`

Details of codes, results and demo： https://github.com/JasmineZhen218/ADproject/blob/master/MultiResolution/readme.md
