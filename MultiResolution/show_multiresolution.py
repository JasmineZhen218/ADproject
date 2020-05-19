# -*- coding: utf-8 -*-
"""
Created on Tue May  5 12:02:23 2020

@author: Jasmine
"""
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from scipy.ndimage import gaussian_filter
def show_local_average(Sb1,Pb1,Sb2,Pb2):
    cmap=cm.get_cmap()
# =============================================================================
#     Sb1[Sb1==0]=np.min(Sb1[Sb1>0])
#     Sb2[Sb2==0]=np.min(Sb2[Sb2>0])
#     
#     Sb1=np.log(Sb1)
#     Sb2=np.log(Sb2)
# =============================================================================
    vmin1=np.min(Sb1)
    vmax1=np.max(Sb1)
    vmin2=np.min(Sb2)
    vmax2=np.max(Sb2)    
    vmin=min(vmin1,vmin2)
    vmax=max(vmax1,vmax2)
    Sb01_1=(Sb1-vmin)/(vmax-vmin)
    Sb01_2=(Sb2-vmin)/(vmax-vmin)
    RGBA_1=cmap(Sb01_1)
    RGBA_1[...,-1]=Pb1/np.max(Pb1)
    RGBA_2=cmap(Sb01_2)
    RGBA_2[...,-1]=Pb2/np.max(Pb2)   
    
    f1,ax1 = plt.subplots()
    h=ax1.imshow(RGBA_1)
    cb = plt.colorbar(h)
    ticks = cb.get_ticks()
    cb.set_ticks(ticks)
    cb.set_ticklabels(ticks*(vmax-vmin) + vmin)
    ax1.set_title("Local average (Tau tangle)")
    
    f2,ax2 = plt.subplots()
    h=ax2.imshow(RGBA_2)
    cb = plt.colorbar(h)
    ticks = cb.get_ticks()
    cb.set_ticks(ticks)
    cb.set_ticklabels(ticks*(vmax-vmin) + vmin)
    ax2.set_title("Local average (Amyloid plaque)")
    plt.show()

def show_local_std(Sstd1,Pb1,Sstd2,Pb2):
# =============================================================================
#     Sstd1[Sstd1==0]=np.min(Sstd1[Sstd1>0])
#     Sstd2[Sstd2==0]=np.min(Sstd2[Sstd2>0])
#     Sstd1=np.log(Sstd1)
#     Sstd2=np.log(Sstd2)
# =============================================================================
    
    cmap=cm.get_cmap()
    
    tmp1=np.mean(Sstd1[Pb1>0])
   
    vmin1=tmp1*0.5
    vmax1=tmp1*2.0 
    tmp2=np.mean(Sstd2[Pb2>0])
    vmin2=tmp2*0.5
    vmax2=tmp2*2.0     
    vmin=min(vmin1,vmin2)
    vmax=max(vmax1,vmax2)
    print(vmin,vmax)
    
    
    Sstd01_1=(Sstd1-vmin)/(vmax-vmin)
    Sstd01_2=(Sstd2-vmin)/(vmax-vmin)
    
    

    RGBA_1=cmap(Sstd01_1)
    RGBA_1[...,-1]=Pb1/np.max(Pb1)
    RGBA_2=cmap(Sstd01_2)
    RGBA_2[...,-1]=Pb2/np.max(Pb2)   
    
    f1,ax1 = plt.subplots()
    h=ax1.imshow(RGBA_1)
    cb = plt.colorbar(h)
    ticks = cb.get_ticks()
    cb.set_ticks(ticks)
    cb.set_ticklabels(ticks*(vmax-vmin) + vmin)
    ax1.set_title("Local standard deviation (Tau tangle)")
    
    f2,ax2 = plt.subplots()
    h=ax2.imshow(RGBA_2)
    cb = plt.colorbar(h)
    ticks = cb.get_ticks()
    cb.set_ticks(ticks)
    cb.set_ticklabels(ticks*(vmax-vmin) + vmin)
    ax2.set_title("Local standard deviation (Amyloid plaque)")

    
root="D:/Brain2/down_002/"
particle_names=["tau","amyloid"]
path1=root+particle_names[0]+"/"
path2=root+particle_names[1]+"/"
# =============================================================================
# feature_names=["size_map","roundness_map","orientation_map"]
# Sigma=[100,200,500]
# =============================================================================
feature_names=["roundness_map"]
Sigma=[500]
prob_map1=np.load(path1+"prob.npy")
prob_map2=np.load(path2+"prob.npy")
for i in range(len(feature_names)):
    for sigma in Sigma:
        print(feature_names[i],sigma,"...")
        prob_blur1=np.load(path1+'_prob_blur_'+str(sigma)+".npy") 
        prob_blur2=np.load(path2+'_prob_blur_'+str(sigma)+".npy") 
        local_mean1=np.load(path1+feature_names[i]+'_local_mean_'+str(sigma)+".npy") 
        local_mean2=np.load(path2+feature_names[i]+'_local_mean_'+str(sigma)+".npy") 
        show_local_average(local_mean1,prob_blur1,local_mean2,prob_blur2)
        
        
# =============================================================================
#         local_std1=np.load(path1+feature_names[i]+'_local_std_'+str(sigma)+".npy") 
#         local_std2=np.load(path2+feature_names[i]+'_local_std_'+str(sigma)+".npy")         
#         show_local_std(local_std1,prob_blur1,local_std2,prob_blur2)
# =============================================================================



    