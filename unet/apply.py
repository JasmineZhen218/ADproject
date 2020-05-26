# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 19:29:18 2020

@author: Jasmine

This code is used to conduct semantic segmentation on an AD pathology image using pre-trained models.
It takes 3 arguments from command line:
    1) The path of pathology image to segment
    2) The path of pre-trained model to apply
    3) The path to save the output probability map
"""
import torch
import sys
from Unet_arch import *
import matplotlib.image as mpimg
import numpy as np
import cv2
from PIL import Image
Image.MAX_IMAGE_PIXELS=None

def image2sample(image):
    # convert to torch
    img_tensor=torch.as_tensor(image.transpose((2,0,1)),dtype=torch.float)
    C,H,W=img_tensor.shape
    sample =torch.zeros(1,C,H,W)
    sample[0,:,:,:]=img_tensor
    return sample


def apply(img_path,model_path):
    hist=mpimg.imread(img_path)
    # load unet
    unet = UNet(in_ch=3,    # number of channels in input image, RGB=3
            out_ch=2,   # number of channels in output image,
                        # classification here is forground or background=2
            first_ch=8, # how many features at the first layer
            nmin=9,     # minimum image size, this will define
         # how many times do we need to downsample by a factor of 2
          )
    unet.load_state_dict(torch.load(model_path))
    print(unet)
    
    h=hist.shape[0]
    w=hist.shape[1]
    #print("image shape:",h,w)
    # flip padding
    p_hist=cv2.copyMakeBorder(hist,44,88-h%44,44,88-w%44,cv2.BORDER_REFLECT)
    p_h=p_hist.shape[0]
    p_w=p_hist.shape[1]

    # apply unet
    prob_map=np.zeros((h+44-h%44,w+44-w%44))
    nblock_a1=int(p_h/44)-2
    nblock_a2=int(p_w/44)-2

    for i in range(nblock_a1):
        for j in range(nblock_a2):

            block=p_hist[i*44:i*44+132,j*44:j*44+132]
            unet_input=image2sample(block)
            unet_output=unet(unet_input)
            # final activation
            prob_block=torch.softmax(unet_output.detach(),dim=1)[0,1].numpy()
            prob_map[i*44:(i+1)*44,j*44:(j+1)*44]=prob_block
    
    prob_map=prob_map[:h,:w]
    return prob_map


def main(argv):
    input_path=argv[0]
    model_path=argv[1]
    output_path=argv[2]
    print("We are going to conduct semantic segmentation on: ", input_path)
    print("The model applied is: ", model_path)
    print("Caculating probability map ...")
    prob_map=apply(input_path,model_path)
    print("Finish calculation")
    print("The output probability map will be saved in: ", output_path)
    np.save(output_path,prob_map)


   
if __name__=="__main__":
    main(sys.argv[1:])