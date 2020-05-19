# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 06:29:52 2020

@author: Jasmine
"""
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg
import pandas as pd
root="D:/Brain2/down_000/_002/AD_Hip1/Amyloid/location5_part_"
subdir="000_000/"
suffix="Block1_amyloid_location5_part_000_000_"
description_path=root+subdir+suffix+"description.csv"
feature_name=["base_map.tif","prob.jpg",
              "_object_map.npy","_size_map.npy",
              "_roundness_map.npy","_orientation_map.npy"]
title=["Base","Probability map",
       "Binary Segmentation","Size map",
       "Roundness map","Orientation map"]

description=pd.read_csv(description_path)

print(suffix)
f1,((ax1,ax2),(ax3,ax4),(ax5,ax6))=plt.subplots(3,2,figsize=(20,20))
ax=[ax1,ax2,ax3,ax4,ax5,ax6]
for i in range(len(ax)):
    if i==0 or i==1:
        feature_map_path=root+subdir+'feature_map/'+suffix+feature_name[i]
        feature_map=mpimg.imread(feature_map_path)
    else:
        feature_map_path=root+subdir+'feature_map/'+suffix+feature_name[i]
        feature_map=np.load(feature_map_path)
    ax[i].imshow(feature_map)
    ax[i].set_title(title[i])
f1.show()

print("Slide Summary:")
print(description[['area','roundness','orientation']].describe())    
f2,(ax1,ax2,ax3)=plt.subplots(1,3,figsize=(15,5))
ax1.hist(description.area)
ax1.set_title("Histogram of area")
ax2.hist(description.roundness)
ax2.set_title("Histogram of roundness")
ax3.hist(description.orientation)
ax3.set_title("Histogram of orientation")
f2.show()