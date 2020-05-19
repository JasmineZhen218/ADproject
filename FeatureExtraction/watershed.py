# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 08:38:03 2020

@author: Jasmine
"""
import cv2
import numpy as np

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
    #print(prob_sample_c3.dtype)
    #print(markers.dtype)
    segmented=cv2.watershed(prob_sample_c3,markers)
    return segmented