# Multiresolution analysis

The goal of this section is to reconstruct feature map from the `description.csv` files and conduct multiresolution analysis. From each `description.csv`, 3 feature maps including `Size_map.npy`, `Roundness_map.npy` and `Orientation_map.npy` would be reconstructed from.  The second part is to extract texture of each feature map by calculating the probability-weighted local mean and local standard deviation using gaussian filters.

### Reconstruct feature map

#### Algorithm

The reconstruction is conducted by filling the biomarker region with feature values. For example, when we construct size map. The script will fill the region where Biomarker #1 occupied with the size of Biomarker #1.

#### Input

[1] `Segmented.npy`: It is  a 1-channel NDARRAY file which is the result of applying Watershed algorithm to probability map. 

[2] `description.csv`:  It is a `csv` file which records the features of each segmented biomarker.

#### How to run the code

To  reconstruct feature maps, run the script `fill_feature_maps`. It takes 3 arguments:

[1] input_csv_path: path to the description map

[2] input_segmented_path: path to the `Segmented.npy`

[3] output_path: path to a directory which the feature maps will be saved

An example to run the script:

```
python fill_feature_maps.py asset/description.csv asset/Segmented.npy asset/FeatureMaps 
```

#### Output

All the reconstructed feature maps are saved in the 3rd argument you specified when running `fill_feature_map.py`. In the example above, the directory would be `asset/FeatureMaps/`

In that directory, there are 3 constructed feature maps:

[1] `Size_map.npy`: It is a 1-channel NDARRAY

[2] `Orientation_map.npy`: It is a 1-channel NDARRAY

[3] `Roundness_map.npy`: It is a 1-channel NDARRAY



### Texture extraction

#### Algorithm

We will calculate probability weighted local average and local standard deviation of each feature map. Local average and local standard deviation are good methods to extract **abstract textures** of feature maps.

The formula are shown below:

```
local_mean_I=gaussian_filter(feature_map*prob,sigma)/prob_blur
local_mean_I2=gaussian_filter(feature_map**2*prob, sigma)/prob_blur
local_deviation=local_mean_I2 - local_mean_I**2
local_deviation[local_deviation<0]=0
local_standard_deviation = np.sqrt(local_deviation)
```

>  `prob_blur` indicates the blur version of probability map.

The reason to incorporate information from probability map when calculating local mean and local standard deviation is that we want to repress information from regions where we have low confidence that there are biomarkers when we extract textures.

#### Input

To conduct extract textures of feature maps, ensure these 4 files exist in the same directory:

[1] `Prob_map.npy`

[2] `Roundness_map.npy`

[3] `Size_map.npy`

[4] `Roundness_map.npy`

#### How to run the code

To conduct extract textures of feature maps, run the script `texture_extraction.py`. It takes  2 arguments:

[1] Path to the directory which contains all 4 files mentioned in input section

[2] Sigma of Gaussian filter to apply. We suggest sigma=200 as it is large enough to extract textures of feature maps after testing. The larger the sigma is, the calculation would be slower.

An example to run the code:

```
python texture_extraction.py asset/FeatureMaps 200
```

##### Output

If you specify sigma=200, then output would be:

>  [1] `Prob_map_blur_200.0.npy`
>
> [2] `Roundness_map_local_mean_200.0.npy`
>
> [3]`Roundness_map_local_std_200.0.npy`
>
> [4]`Size_map_local_mean_200.0.npy`
>
> [5] `Size_map_local_std_200.0.npy`
>
> [6] `Orientation_map_local_mean_200.0.npy`
>
> [7] `Orientation_map_local_std_200.0.npy`



To visualize these output and see how they show the texture of feature maps, see https://drive.google.com/open?id=14VF4EpjGUQdoCBzw6vASqGO29LwNcBZk

