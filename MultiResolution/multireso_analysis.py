# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 14:07:03 2020

@author: Jasmine
"""

from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg
import pandas as pd

def local_standard_deviation(image,prob,prob_blur,sigma):
    local_mean_I=gaussian_filter(image*prob,sigma)/prob_blur
    local_mean_I2=gaussian_filter(image**2*prob, sigma)/prob_blur
    local_deviation=local_mean_I2 - local_mean_I**2
    local_deviation[local_deviation<0]=0
    local_standard_deviation = np.sqrt(local_deviation)
    return  local_mean_I,local_standard_deviation


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

# =============================================================================
# feature_name=["size_map","roundness_map","orientation_map"]
# Sigma=[100,200,500]
# =============================================================================

feature_name=["roundness_map"]
Sigma=[100,200,500]
# =============================================================================
# feature_name=["size_map.npy"]
# Sigma=[100]
# =============================================================================

import matplotlib.cm as cm

def show_local_average(Sb,Pb):
    cmap=cm.get_cmap()
    vmin=np.min(Sb)
    vmax=np.max(Sb)
    Sb01=(Sb-vmin)/(vmax-vmin)
    
    RGBA=cmap(Sb01)
    RGBA[...,-1]=Pb/np.max(Pb)
    f,ax = plt.subplots()
    h = ax.imshow(RGBA)

    # add colorbar
    cb = plt.colorbar(h)
    # the tick labels just show 0 to 1, now fix them
    ticks = cb.get_ticks()
    cb.set_ticks(ticks)
    cb.set_ticklabels(ticks*(vmax-vmin) + vmin)

def show_local_std(Sstd,Pb):
    tmp=np.mean(Sstd[Pb>0])
    vmin=tmp*0.5
    vmax=tmp*2.0 
    Sstd01=(Sstd-vmin)/(vmax-vmin)
    
    cmap=cm.get_cmap()
    RGBA=cmap(Sstd01)
    RGBA[...,-1]=Pb/np.max(Pb)
    
    f,ax = plt.subplots()
    h = ax.imshow(RGBA)
    cb = plt.colorbar(h)

    ticks = cb.get_ticks()
    cb.set_ticks(ticks)
    cb.set_ticklabels(ticks*(vmax-vmin) + vmin)
    ax.set_title('Local std of signal with transparency')
# =============================================================================
# feature_map=np.load(root+subdir+'feature_map/'+suffix+feature_name[5])
# =============================================================================
# =============================================================================
# f,(ax1,ax2)=plt.subplots(2,1,figsize=(20,10))
# ax=[ax1,ax2,ax3,ax4]
# =============================================================================
for i in range(len(feature_name)):
    for sigma in Sigma:
        print(feature_name[i],sigma,"...")
        prob_map=np.load(save_path+"prob.npy")
        print(np.min(prob_map))
        feature_map=np.load(save_path+feature_name[i]+".npy")
        prob_blur=gaussian_filter(prob_map,sigma)
        local_mean,local_std_map=local_standard_deviation(feature_map,prob_map,prob_blur,sigma)
        print(np.min(local_mean))
        #show_local_average(local_mean,prob_blur)
        #show_local_std(local_std_map,prob_blur)
        np.save(save_path+feature_name[i]+'_local_mean_'+str(sigma)+'.npy',local_mean)
        np.save(save_path+'_prob_blur_'+str(sigma)+'.npy',prob_blur)
        np.save(save_path+feature_name[i]+'_local_std_'+str(sigma)+'.npy',local_std_map)

# =============================================================================
# for i in range(len(ax)):
#     if i==0 or i==1:
#         feature_map_path=root+subdir+'feature_map/'+suffix+feature_name[i]
#         feature_map=mpimg.imread(feature_map_path)
#     else:
#         feature_map_path=root+subdir+'feature_map/'+suffix+feature_name[i]
#         feature_map=np.load(feature_map_path)
# =============================================================================
