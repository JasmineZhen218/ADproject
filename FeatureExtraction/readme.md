# Feature extraction

The goal of this section is to segment individual biomarkers from probability map using watershed algorithm and descript each biomarker using their position, size, orientation and roundness. 

### Input

[1] `Prob_map.npy`:  It is a 1-channel NDARRAY file which is the output of applying pre-trained UNET model to unlabeled pathology image. The value of each pixel represents the probability of being a biomarker here.

**Note: The original probability map has the same size with pathology image, which may be too large for down streaming analysis. We suggested to down sample it by 2 in row and column before feature extraction.**

### How to run the code

To extract individual biomarkers and describe them, run the script `feature_extraction.py`. It takes three arguments:

​        [1] Path to read in probability map

​        [2] Path to save the result of segmentation

​		[3] Path to save the description csv

An example to run the script:

```
feature_extraction.py asset/Prob_map.npy asset/Segmented.npy asset/description.csv
```

### Output

[1] `Segmented.npy` : It is  a 1-channel NDARRAY file which is the result of applying Watershed algorithm to probability map. All the pixels are integers. 

> * 1 represents background; 
> * -1 represents contour of biomarkers; 
> * {2,3,4,5...N} represents segmented biomarkers; 
> * 0 represents unsure pixels. Normally, unsure pixels should take up a extreme small portion of all the pixels(<0.01%).

[2] `description.csv`: It is a `csv` file which records the features of each segmented biomarker. There are 12 columns in all.

> `ID`: the ID assigned to a biomarker
>
> `upperLeft_x`, `upperLeft_y`, `bottomRight_x`, `bottomRight_y`: The four corners of a small bounding box which bounds the biomarker
>
> `local_center_x`, `local_center_y`: The center of biomarker within the bounding box
>
> `global_center_x`, `global_center_y`: The center of biomarker in the whole image
>
> `area`: Area of the biomarker
>
> `orientation`: Orientation of the biomarker
>
> `roundness`: Roundness of the biomarker

### Methods 

2. Biomarker segmentation: [watershed algorithm in OpenCV-python](https://docs.opencv.org/master/d3/db4/tutorial_py_watershed.html) is applied to down sampled version of probability map.

3. Feature extraction: Each biomarker is described using position, size, orientation and roundness. To see detail geometry derivation, [???]

