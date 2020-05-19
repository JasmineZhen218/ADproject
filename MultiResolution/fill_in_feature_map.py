# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 05:56:04 2020

@author: Jasmine
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import imageio

particle_name="amyloid"
block=1
location=5
root="D:/Brain2/down_002/"
if particle_name=="amyloid":       
    base_path=root+"amyloid.tif"
elif particle_name=="tau":
    base_path=root+"tau.tif"
else:
    print("Invalid particel name")
save_path=root+particle_name+'/'
descriptions=pd.read_csv(save_path+"description.csv")
descriptions=descriptions.loc[descriptions.area>1]
segmented=np.load(save_path+"segmented.npy")
length,width=segmented.shape

def fill(label,feature,include_contour=False):
    # label: bg 1, contour -1, tangle 2 or 3 or 4
    label_new=label.copy()
    if include_contour:
        label_new[label==1]=0
        label_new[label!=1]=1
    else:
        label_new[label==1]=0
        label_new[label==-1]=0
        label_new[label>1]=feature
    return label_new
# distribution map
object_map=np.zeros((length,width))
for index,row in descriptions.iterrows():
    try:
        ID=int(row.ID)
        upperLeft_x=int(row.upperLeft_x)
        upperLeft_y=int(row.upperLeft_y)
        bottomRight_x=int(row.bottomRight_x)
        bottomRight_y=int(row.bottomRight_y)
        label=segmented[upperLeft_y:bottomRight_y,upperLeft_x:bottomRight_x]
        label_to_paste=fill(label,1)
        object_map[upperLeft_y:upperLeft_y+label_to_paste.shape[0],
             upperLeft_x:upperLeft_x+label_to_paste.shape[1]]=label_to_paste
    except:
        print("Object Fail in Num.", ID)
# size map
size_map=np.zeros((length,width))
for index, row in descriptions.iterrows():
    try:
        ID=int(row.ID)
        area=row.area
        upperLeft_x=int(row.upperLeft_x)
        upperLeft_y=int(row.upperLeft_y)
        bottomRight_x=int(row.bottomRight_x)
        bottomRight_y=int(row.bottomRight_y)
        label=segmented[upperLeft_y:bottomRight_y,upperLeft_x:bottomRight_x]   
        label_to_paste=fill(label,area)
        size_map[upperLeft_y:upperLeft_y+label_to_paste.shape[0],
             upperLeft_x:upperLeft_x+label_to_paste.shape[1]]=label_to_paste
    except:
        print("Size, Fail in Num.",ID)
# roundness map
roundness_map=np.zeros((length,width))
for index, row in descriptions.iterrows():
    ID=int(row.ID)
    upperLeft_x=int(row.upperLeft_x)
    upperLeft_y=int(row.upperLeft_y)
    roundness=row.roundness
    #print(roundness)
    bottomRight_x=int(row.bottomRight_x)
    bottomRight_y=int(row.bottomRight_y)
    label=segmented[upperLeft_y:bottomRight_y,upperLeft_x:bottomRight_x]
    label_to_paste=fill(label,roundness)
    roundness_map[upperLeft_y:upperLeft_y+label_to_paste.shape[0],
             upperLeft_x:upperLeft_x+label_to_paste.shape[1]]=label_to_paste
# =============================================================================
#     except:
#         print("Roundness,Fail in Num.",ID)
# =============================================================================
# orientation m
orientation_map=np.zeros((length,width))
for index, row in descriptions.iterrows():
    try:
        ID=int(row.ID)
        upperLeft_x=int(row.upperLeft_x)
        upperLeft_y=int(row.upperLeft_y)
        bottomRight_x=int(row.bottomRight_x)
        bottomRight_y=int(row.bottomRight_y)
        orientation=row.orientation
        label=segmented[upperLeft_y:bottomRight_y,upperLeft_x:bottomRight_x]
        label_to_paste=fill(label,orientation)
        orientation_map[upperLeft_y:upperLeft_y+label_to_paste.shape[0],
                        upperLeft_x:upperLeft_x+label_to_paste.shape[1]]=label_to_paste
    except:
        print("Orientation,Fail in Num.",ID)
               
# save
#imageio.imsave(feature_map_path+'_object_map.jpg',object_map)
np.save(save_path+'object_map.npy',object_map)
#imageio.imsave(feature_map_path+'_size_map.jpg',size_map)
np.save(save_path+'size_map.npy',size_map)
#imageio.imsave(feature_map_path+'_roundness_map.jpg',roundness_map)
np.save(save_path+'roundness_map.npy',roundness_map)
#imageio.imsave(feature_map_path+'_orientation_map.jpg',orientation_map)
np.save(save_path+'orientation_map.npy',orientation_map)



