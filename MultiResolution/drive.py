# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 22:22:25 2020

@author: Jasmine
"""

#from apply import *
import watershed as ws
import get_attribute as ga
import cv2
import pandas as pd
import numpy as np
import sys

def extract1tangle(segmented,label):
    y_min=min(np.where(segmented==label)[0])
    y_max=max(np.where(segmented==label)[0])
    x_min=min(np.where(segmented==label)[1])
    x_max=max(np.where(segmented==label)[1])
    
    if y_min-2>=0:
        y_min-=2
    if x_min-2>=0:
        x_min-=2
    if y_max+3<=segmented.shape[0]:
        y_max+=3
    if x_max+3<=segmented.shape[1]:
        x_max+=3     
    upperLeft=(x_min,y_min)
    bottomRight=(x_max,y_max)
    crop=segmented[y_min:y_max,x_min:x_max]
    return upperLeft, bottomRight,crop


def get_descriptions(prob_map):
    segmented=ws.cv_watershed(prob_map)
    unsure_pixels=np.where(segmented==0)
    print("Unsure pixels:", unsure_pixels)
    df=pd.DataFrame()
    labels=[i for i in np.unique(segmented).tolist() if i!=-1 and i!=1 and i!=0] 
    print("There are {} particles in all".format(len(labels)))
    for index in range(len(labels)):  
        ID=index+1
        label=labels[index]
        upperLeft, bottomRight, crop=extract1tangle(segmented,label)
        binary_crop=ga.preprocess(crop)
        position,area=ga.get_position_area(binary_crop)
        theta,roundness=ga.orientation_and_roundness(binary_crop)
        print(ID, position, area, theta, roundness)
     
        df.loc[index,'ID']=ID
        df.loc[index,'upperLeft_x']=upperLeft[0]
        df.loc[index,'upperLeft_y']=upperLeft[1]
        df.loc[index,'bottomRight_x']=bottomRight[0]
        df.loc[index,'bottomRight_y']=bottomRight[1]
        df.loc[index,'local_center_x']=position['x']
        df.loc[index,'local_center_y']=position['y'] 
        df.loc[index,'global_center_x']=upperLeft[0]+position['x']
        df.loc[index,'global_center_y']=upperLeft[1]+position['y']
        df.loc[index, 'area']=area
        df.loc[index, 'orientation']=theta
        df.loc[index, 'roundness']=roundness
    return segmented,df


def main():
    particle_name="amyloid"
    block=1
    location=5
    
    
    #input path
    root="D:/Brain2/down_002/"
    if particle_name=="amyloid":       
        base_path=root+"amyloid.tif"
        model_path="../asset/unet_amyloid2.pth"
    elif particle_name=="tau":
        base_path=root+"tau.tif"
        model_path="../asset/unet_tau_nw.pth"
    else:
        print("Invalid particel name")
    
    # output path
    save_path=root+particle_name+'/'
    
    print("Start applying model to pathology slide.....")
# =============================================================================
#     prob_map=apply(base_path,model_path)
#     np.save(save_path+"prob.npy", prob_map)
# =============================================================================
    prob_map=np.load(save_path+"prob.npy")
    print("Maximum of probability={}, minimum probability={}".format(np.max(prob_map),np.min(prob_map)))
    segmented,descriptions=get_descriptions(prob_map)
    
    np.save(save_path+"segmented.npy",segmented)
    descriptions.to_csv(save_path+"description.csv",index=False)

    
if __name__=="__main__":
    main()

