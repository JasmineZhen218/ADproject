# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 14:07:03 2020

@author: Jasmine
"""

import numpy as np
import os
import sys
from scipy.ndimage import gaussian_filter

def prob_weighted_local_average_and_local_mean(feature_map,prob,prob_blur,sigma):
    
    local_mean_I=gaussian_filter(feature_map*prob,sigma)/prob_blur
    local_mean_I2=gaussian_filter(feature_map**2*prob, sigma)/prob_blur
    local_deviation=local_mean_I2 - local_mean_I**2
    local_deviation[local_deviation<0]=0
    local_standard_deviation = np.sqrt(local_deviation)
    return  local_mean_I,local_standard_deviation



def main(argv):
    input_feature_path=argv[0]
    sigma=float(argv[1])
    print("We are going to deal with feature maps in ", input_feature_path)
    
    
    print("Blurring the probability map using a gaussian filter of sigma={}".format(sigma))
    prob_map=np.load(os.path.join(input_feature_path,'Prob_map.npy'))
    prob_blur=gaussian_filter(prob_map,sigma)
    np.save(os.path.join(input_feature_path,'Prob_map_blur_'+str(sigma)+'.npy'),prob_blur)
    print("Finish blurring, the blurred version of probability map has been saved in ", input_feature_path)
    
# =============================================================================
#     print("Calculating probability weighted Local mean and Local standard deviation of size map ...")
#     Size_map=np.load(os.path.join(input_feature_path,'Size_map.npy'))
#     local_mean,local_std=prob_weighted_local_average_and_local_mean(Size_map,prob_map,prob_blur,sigma)    
#     np.save(os.path.join(input_feature_path,'Size_map_local_mean_'+str(sigma)+'.npy'),local_mean)
#     np.save(os.path.join(input_feature_path,'Size_map_local_std_'+str(sigma)+'.npy'),local_std)
#     print("Finished calculating, local mean and local std have been saved in ", input_feature_path)
#     
#     print("Calculating probability weighted Local mean and Local standard deviation of orientation map ...")
#     Orientation_map=np.load(os.path.join(input_feature_path,'Orientation_map.npy'))
#     local_mean,local_std=prob_weighted_local_average_and_local_mean(Orientation_map,prob_map,prob_blur,sigma)    
#     np.save(os.path.join(input_feature_path,'Orientation_map_local_mean_'+str(sigma)+'.npy'),local_mean)
#     np.save(os.path.join(input_feature_path,'Orientation_map_local_std_'+str(sigma)+'.npy'),local_std)
#     print("Finished calculating, local mean and local std have been saved in ", input_feature_path)
# =============================================================================
    
    print("Calculating probability weighted Local mean and Local standard deviation of roundness map ...")
    Roundness_map=np.load(os.path.join(input_feature_path,'Roundness_map.npy'))
    local_mean,local_std=prob_weighted_local_average_and_local_mean(Roundness_map,prob_map,prob_blur,sigma)    
    np.save(os.path.join(input_feature_path,'Roundness_map_local_mean_'+str(sigma)+'.npy'),local_mean)
    np.save(os.path.join(input_feature_path,'Roundness_map_local_std_'+str(sigma)+'.npy'),local_std)
    print("Finished calculating, local mean and local std have been saved in ", input_feature_path)
    
if __name__=="__main__":
    main(sys.argv[1:])