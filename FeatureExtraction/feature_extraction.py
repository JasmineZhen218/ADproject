# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 22:22:25 2020

@author: Jasmine
"""


import cv2
import pandas as pd
import numpy as np
import sys
#from skimage.transform import downscale_local_mean


def stack(image_c1):
    image_c3=np.zeros((image_c1.shape[0],image_c1.shape[1],3))
    for i in range(3):
        image_c3[:,:,i]=image_c1
    image_c3=image_c3.astype(np.uint8)
    return image_c3

def cv_watershed(prob_sample):
    prob_sample=cv2.normalize(prob_sample,None,alpha=0,beta=255,
                              norm_type=cv2.NORM_MINMAX,dtype=cv2.CV_8UC1)
    ret,binary_sample=cv2.threshold(prob_sample,0,255,cv2.THRESH_OTSU)
    ret,markers_cp=cv2.connectedComponents(binary_sample)
    kernel=np.ones((3,3),np.uint8)
    #dilation
    sure_bg=cv2.dilate(binary_sample,kernel)
    #erison
    sure_fg=cv2.erode(binary_sample,kernel)
    #unrure
    unknown=cv2.subtract(sure_bg,sure_fg)
    ret,markers=cv2.connectedComponents(sure_fg)
    markers=markers+1
    markers[unknown==255]=0
    prob_sample_c3=stack(prob_sample)
    segmented=cv2.watershed(prob_sample_c3,markers)
    return segmented

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


def preprocess(label,include_contour=False):
    # label: bg 1, contour -1, tangle 2 or 3 or 4
    label_new=label.copy()
    if include_contour:
        label_new[label==1]=0
        label_new[label!=1]=1
    else:
        label_new[label==1]=0
        label_new[label==-1]=0
        label_new[label>1]=1
    return label_new

def get_position_area(label):
    H,W=label.shape
    area=np.sum(label)
    x_array=np.zeros(label.shape)
    y_array=np.zeros(label.shape)
    for x in range(W):
        x_array[:,x]=x
    for y in range(H):
        y_array[y,:]=y
    x_mean=np.sum(x_array*label)/area
    y_mean=np.sum(y_array*label)/area
    position={'x':x_mean,'y':y_mean}
    return position,area

def orientation_and_roundness(label):
    def energy(a,b,c,theta):
        return a*np.sin(theta)**2-b*np.sin(theta)*np.cos(theta)+c*np.cos(theta)**2
    H,W=label.shape
    #print(np.unique(label))
    area=np.sum(label)
    x_array=np.zeros(label.shape)
    y_array=np.zeros(label.shape)
    for x in range(W):
        x_array[:,x]=x
    for y in range(H):
        y_array[y,:]=y
        
    x_mean=np.sum(x_array*label)/area
    y_mean=np.sum(y_array*label)/area
    
    x_prime=x_array-x_mean
    y_prime=y_array-y_mean
    a=np.sum(x_prime*x_prime*label)
    b=2*np.sum(x_prime*y_prime*label)
    c=np.sum(y_prime*y_prime*label)
    theta_min=1/2*np.arctan2(b,a-c)
    theta_max=theta_min+np.pi/2
    # calculate roundnes 
    E_min=energy(a,b,c,theta_min)
    E_max=energy(a,b,c,theta_max)
    roundness=E_min/E_max
    return theta_max, roundness




def get_descriptions(segmented):
    unsure_pixels=np.where(segmented==0)
    print("There are {} unsure pixels:".format(len(unsure_pixels)))
    df=pd.DataFrame()
    labels=[i for i in np.unique(segmented).tolist() if i!=-1 and i!=1 and i!=0] 
    print("There are {} particles in all".format(len(labels)))
    ID=1
    for index in range(len(labels)):  
        print("Describing the {}th biomarker".format(index))
        label=labels[index]
        upperLeft, bottomRight, crop=extract1tangle(segmented,label)
        binary_crop=preprocess(crop)
        position,area=get_position_area(binary_crop)
        if area<=1:
            continue
        theta,roundness=orientation_and_roundness(binary_crop)
        #print(ID, position, area, theta, roundness)
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
        
        ID+=1
    return df


def main(argv):
    """
    Arguments:
        [1] input_path: path to read in probability 
        [2] output_segemented_path: path to save the result of watershed segmentation
        [3] output_csv_path: path to save the description csv
    """
    input_path=argv[0]
    output_segmented_path=argv[1]
    output_csv_path=argv[2]   
    print("We are going to deal with ", input_path)
    prob_map=np.load(input_path)
    
    print("Segmenting biomarkers on downsampling version....")
    segmented=cv_watershed(prob_map)
    np.save(output_segmented_path,segmented)
    print("Finish segmentation, the segmented result has been be save in ",output_segmented_path)
    
    print("Describing biomarkers on downsampling version...")
    descriptions=get_descriptions(segmented)
    descriptions.to_csv(output_csv_path,index=False)
    print("Finish description, the description csv file has been save in ",output_csv_path)
    
if __name__=="__main__":
    main(sys.argv[1:])

