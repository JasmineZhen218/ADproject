# AD pathology analysis

This is a repository for processing and analyzing pathology images of Alzheimer disease(AD) patients. There are three sections:

### Image preprocessing

The goal of this section is to prepare training dataset for training neural network in the next step. The large pathology images were cropped into small pieces. Pieces and their pixel-wise labelling were saved. 

Details of codes, data and demo: 

### Semantic segmentation using UNET

The goal of this section is to train UNET models using annotated images and then apply pretrained models to unlabeled images to form a probability map. The value of each pixel on that map represents the probability of being a biomarker or not.

* STEP1: Train UNET models and evaluate performance
* STEP2: Apply satisfactory UNET models to unlabeled images to form probability map

Detailed of codes , pretrained  models and demo: 

### Feature extraction

The goal of this section is to extract every biomarkers from probability map  and describe their size, location, orientation and roundness.

* STEP1: Use watershed to get the clear contour of each biomarker from probability map
* STEP2: Assign an ID and describe each biomarker and save the [ID: features] in to `description.csv` files 

Detailed of codes, results and demo: 

### Multiresolution analysis

The goal of this section is to reconstruct feature map from the `description.csv` files and conduct multiresolution analysis

* STEP1: Reconstruct feature map by "filling" each biomarker with its corresponding features. There would be one feature map for each feature, such as `size_map`, `orientation_map`.
* STEP:  Calculate local average and local standard deviation on these maps using Gaussian smoothing with various `sigma`

Details of codes, results and demo： 