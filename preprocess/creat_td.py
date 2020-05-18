#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 10:48:41 2020

@author: zwang
"""
import sys
import matplotlib.image as mpimg
import numpy as np
import nibabel as nib
from skimage import measure
import random
import os

def crop(image,bbox):
    if len(image.shape)==3:
        return image[bbox[0]:bbox[2],bbox[1]:bbox[3],:]
    elif len(image.shape)==2:
        return image[bbox[0]:bbox[2],bbox[1]:bbox[3]]
    else:
        print("Image dimension wrong!")
        return 0

def labeledRegion(base,zone_sample,label):
    """
    if the base is not labeled anywhere, first extract labeled regions
    arg:
        base:base image
        sz: image to indicate where are labeled
        label: label images
    return: 
        base_images: a list of base pieces
        label_images: a list of label pieces
    """
    labeled_region,region_num=measure.label(zone_sample,return_num=True)
    #  Measure.label return a list of RegionProperties,
    #  Each item describes one labeled region, 
    #  Can be accessed using the attributes listed below
    #  Here, we use the bbox: Bounding box (min_row, min_col, max_row, max_col) 
    proper=measure.regionprops(labeled_region)
    base_list=[]
    label_list=[]
    for item in proper:
        base_list.append(crop(base,item.bbox))
        label_list.append(crop(label,item.bbox))
    return base_list,label_list

def extract_one_sample(base,label,sample_size):
    H,W=label.shape[:2]
    h,w=sample_size
    #print(base.shape)
    #print(label.shape)
    #print(h,w)
    sample=np.zeros((h,w,4),dtype=np.uint8)
    x=random.randrange(W-w)
    y=random.randrange(H-h)
    sample[:,:,0:3]=base[y:y+h,x:x+w,:]
    sample[:,:,3]=label[y:y+h,x:x+w]
    return sample

def write_one_sample(sample,accumulator,save_path):
    sampleName=str(accumulator)+'.npy'
    np.save(save_path+'/'+sampleName,sample)


def create_dataset(base,zone_sample,label,save_path,sample_num,accumulator,sample_size):
    if zone_sample is not None:
        base_list,label_list=labeledRegion(base,zone_sample,label)
    else:
        base_list=[base]
        label_list=[label]
    
    regionNum=len(base_list)
    sample_num_eachRegion=int(sample_num/regionNum)
    for i in range(regionNum):
        base_region=base_list[i]
        label_region=label_list[i]
        for j in range(sample_num_eachRegion):
            accumulator+=1
            print("Extracting the {}th sample".format(accumulator))
            sample=extract_one_sample(base_region,label_region,sample_size)
            write_one_sample(sample,accumulator,save_path)

    return accumulator
    

def main(argv):

    sample_num=int(argv[0]) # how many samples you want to extracted from this pathology image
    accumulator=int(argv[1]) # the number of samples having been in `save_path`. 
    input_path=argv[2]
    output_path=argv[3]  # where you want to save these extarcted samples
    
    if len(argv) == 4:
            sample_size=argv[3]
        
    sample_size=(132,132)
    base=mpimg.imread(os.join.path(input_path,"Base.tif"))
    base=base.transpose((1,0,2))
    zone_sample=nib.load(os.join.path(input_path,"SampleZone.nii.gz"))
    label=nib.load(os.join.path(input_path,"Biomarker.nii.gz"))
    zone_sample=zone_sample.get_fdata()
    zone_sample=zone_sample[:,:,0]    
    label=label.get_fdata()
    label=label[:,:,0]
    print(base.shape)
    print(label.shape)
    print("It is going to append samples to the dataset {}".format(save_path))
    print("There has been {} samples in this dataset".format(accumulator))
    accumulator=create_dataset(base,
                   zone_sample,
                   label,
                   output_path,            
                   sample_num,accumulator,sample_size)
    
    print("Sample extraction finished. Now there should be {} samples in that dataset".format(accumulator))
    


if __name__ == '__main__':
  main(sys.argv[1:])
    