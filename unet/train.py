# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 16:39:39 2020

@author: Jasmine
This script is used to train a unet model from scratch or based on a pretrained model
* Train from scratch , it takes 4 arguments:         
        1) Trainset_path: path to training dataset
        2) batch_size: training batch size, recommend 16
        3) nepochs: number of epochs, recommend 3 as the dataset is quite big
        4) model_save_path: path to save the trained model
* Train based on pretrained model. it takes 5 arguments:    
        1) Trainset_path: path to training dataset
        2) batch_size: training batch size, recommend 16
        3) nepochs: number of epochs, recommend 3 as the dataset is quite big
        4) model_save_path: path to save the trained model
        5) model_load_path: path to pretrained model if you don't want to train from scratch

The up-to-date model will be saved

"""

import os
import sys
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from Unet_arch import *



class ToTensor(object) :
    """ convert ndarrays to tensor"""
    def __call__(delf,sample) :
        image,label=sample['image'],sample['label']
        """
        numpy H W C
        torch C H W
        """
        image=image.transpose((2,0,1))
        sample['image']=torch.as_tensor(image,dtype=torch.float)
        sample['label']=torch.as_tensor(label,dtype=torch.long)
        return sample
    
class ADdataset(Dataset):
    def __init__(self,path,transform=None):
        """
        Args:
            path (string): path to dataset
            transform (callable, optional): Optional transform to be applied
                on a sample.
        """
        self.path=path
        self.transform=transform
        
    def __len__(self):
        files=[f for f in os.listdir(self.path) if os.isfile(os.path.join(self.path,f))]
        return len(files)
    
    def __getitem__(self,idx):  
        sample_name=os.path.join(self.root_dir,str(idx)+'.npy')
        sample=np.load(sample_name)
        image=sample[:,:,0:3]
        label=sample[:,:,3]
        
        # just in case in some patches, biomarkers are not marked as 1
        positive=label!=0
        negative=label==0
        label[negative]=0
        label[positive]=1

        Sample={'image':image,"label":label}
        
        if self.transform :
            Sample=self.transform(Sample)           
        return Sample

def train_unet(unet,dataloader,optimizer,loss_fn,nepochs):
    for e in range(nepochs):
        loss_sum=0
        num_iteration=0
        for sample in dataloader:
            I=sample['image']
            J=sample['label']
            Jhat = unet(I)
            ncrop = (J.shape[2] -Jhat.shape[2])//2
            Jc= J[:,ncrop:-ncrop,ncrop:-ncrop]
            loss =loss_fn(Jhat,Jc)
            loss_sum+=loss
            num_iteration+=1
            # update
            optimizer.zero_grad() 
            loss.backward() 
            optimizer.step()
        mean_loss=loss_sum/num_iteration
        print("The {}th epoch, mean loss={}".format(e,mean_loss))        
    return unet


def main(argv):
    """
    Argv:
        1) Trainset_path: path to training dataset
        2) batch_size: training batch size, recommend 16
        3) nepochs: number of epochs, recommend 3 as the dataset is quite big
        4) model_save_path: path to save the trained model
        5) (optional) model_load_path: path to pretrained model if you don't want to train from scratch
    """
    Trainset_path=argv[0]  # path to training dataset
    batch_size=int(argv([1]))
    nepochs=int(argv[2])   # number of epochs
    model_save_path=argv[3] #path to save the trained model
    unet = UNet(in_ch=3, # number of channels in input image, RGB=3
            out_ch=2, # number of channels in output image, classification here is forground or background=2
            first_ch=8, # how many features at the first layer
            nmin=9, # minimum image size, this will define how big our input images need to be (it is printed)
           )
    if len(argv)==4:
        print("We are going to train from scratch")
    elif len(argv)==5:
        model_load_path=argv[4]
        print("We are going to train from the pretrained model: ",model_load_path)
        unet.load_state_dict(torch.load(model_load_path))
    else:
        print("ilegal input argument")
    
    loss_fn=torch.nn.CrossEntropyLoss()
    learning_rate=1e-3
    optimizer = torch.optim.Adam(unet.parameters(), lr=learning_rate)
    AD_DataSet=ADdataset(path=Trainset_path,transform=ToTensor())
    AD_DataLoader=DataLoader(AD_DataSet,batch_size=batch_size,shuffle=True,num_workers=0)
    print("The unet architecture:",unet)
    print("Training....")
    unet=train_unet(unet=unet,
                    dataloader=AD_DataLoader,
                    optimizer=optimizer,
                    loss_fn=loss_fn,
                    nepochs=nepochs)
    torch.save(unet.state_dict(),model_save_path)
    print("Finished!")
    print("New model has been saved in: ", model_save_path)

    
if __name__ == '__main__':
  main(sys.argv[1:])