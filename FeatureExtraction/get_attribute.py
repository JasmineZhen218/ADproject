# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 20:20:06 2020

@author: Jasmine
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


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
    print(np.unique(label))
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
    #print(E_min)
    E_max=energy(a,b,c,theta_max)
    #print(E_max)
    roundness=E_min/E_max
    return theta_max, roundness

def show_position(label,position):
    
    x=position['x']
    y=position['y']
    
    f,ax=plt.subplots()
    ax.imshow(label)
    ax.plot(x,y,'r*')
    
def show_axis(label,theta,position):
    x=position['x']
    y=position['y']
    x_show=np.linspace(3,label.shape[1]-4,101)
    y_show=np.tan(theta)*(x_show-x)+y
    
    f,ax=plt.subplots()
    ax.imshow(label)
    ax.plot(x_show,y_show,theta,linewidth=2)