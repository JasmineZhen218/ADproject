# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 05:56:04 2020

@author: Jasmine
"""
import pandas as pd
import numpy as np
import sys
import os


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
# =============================================================================
# object_map=np.zeros((length,width))
# for index,row in descriptions.iterrows():
#     try:
#         ID=int(row.ID)
#         upperLeft_x=int(row.upperLeft_x)
#         upperLeft_y=int(row.upperLeft_y)
#         bottomRight_x=int(row.bottomRight_x)
#         bottomRight_y=int(row.bottomRight_y)
#         label=segmented[upperLeft_y:bottomRight_y,upperLeft_x:bottomRight_x]
#         label_to_paste=fill(label,1)
#         object_map[upperLeft_y:upperLeft_y+label_to_paste.shape[0],
#              upperLeft_x:upperLeft_x+label_to_paste.shape[1]]=label_to_paste
#     except:
#         print("Object Fail in Num.", ID)
# =============================================================================
# size map
def fill_size_map(descriptions,segmented):
    length,width=segmented.shape
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
    return size_map
# roundness map
def fill_roundness_map(descriptions,segmented):
    length,width=segmented.shape
    roundness_map=np.zeros((length,width))
    for index, row in descriptions.iterrows():
        try:
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
        except:
            print("Roundness,Fail in Num.",ID)
    return roundness_map
# orientation 
def fill_orientation_map(descriptions,segmented):
    length,width=segmented.shape
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
    return orientation_map
               


def main(argv):
    """
    Arguments:
        [1] input_csv_path: path to the description map
        [2] input_segmented_path: path to the `segmented.npy`
        [3] output_path: path to save the feature maps
    """
    input_csv_path=argv[0]
    input_segemented_path=argv[1]
    output_path=argv[2]
    
    print("We are going to reconstruct feature maps from ", input_csv_path)
    descriptions=pd.read_csv(input_csv_path)
    segmented=np.load(input_segemented_path)
   
    print("Reconstructing size map...")
    size_map=fill_size_map(descriptions,segmented)
    np.save(os.path.join(output_path,'Size_map.npy'),size_map)
    print("Finish reconstruction, Size_map has been saved in ", output_path)
    
    print("Reconstructing roundness map...")
    roundness_map=fill_roundness_map(descriptions,segmented)
    np.save(os.path.join(output_path,'Roundness_map.npy'),roundness_map)
    print("Finish reconstruction, Roundness_map has been saved in ", output_path)
    
    print("Reconstructing orientation map...")
    orientation_map=fill_orientation_map(descriptions,segmented)
    np.save(os.path.join(output_path,'Orientation_map.npy'),orientation_map)
    print("Finish reconstruction, Orientation_map has been saved in ", output_path)
    
    
    
if __name__=="__main__":
    main(sys.argv[1:])
