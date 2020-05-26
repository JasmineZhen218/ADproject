# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 14:32:57 2020

@author: Jasmine
"""
import torch
from torch import nn
import torch.nn.functional as F
import torch.optim as optim


class UNet(nn.Module):
    def DCC(self,in_ch,out_ch):
        block=nn.Sequential(
            nn.MaxPool2d(2),
            nn.Conv2d(in_ch,out_ch,3),
            nn.ReLU(),
            nn.Conv2d(out_ch,out_ch,3),
            nn.ReLU()
        )
        return block
    
    def UCC(self,in_ch,out_ch):
        block=nn.Sequential(
            nn.Conv2d(in_ch,out_ch,3),
            nn.ReLU(),
            nn.Conv2d(out_ch,out_ch,3),
            nn.ReLU()  
        )
        return block
        
    def __init__(self,in_ch,out_ch,first_ch,nmin):
        super(UNet,self).__init__()
        self.in_ch=in_ch
        self.out_ch=out_ch
        self.first_ch=first_ch
        self.nmin=nmin
        ### First layer
        self.cinput1=nn.Conv2d(in_ch,first_ch,3)
        self.cinput2=nn.Conv2d(first_ch,first_ch,3)
        ### Downsampling
        self.dcc1=self.DCC(first_ch,first_ch*2)
        self.dcc2=self.DCC(first_ch*2,first_ch*4)
        self.dcc3=self.DCC(first_ch*4,first_ch*8)
        ### transpose
        self.u3=nn.ConvTranspose2d(first_ch*8,first_ch*4,2,stride=2)
        self.u2=nn.ConvTranspose2d(first_ch*4,first_ch*2,2,stride=2)
        self.u1=nn.ConvTranspose2d(first_ch*2,first_ch*1,2,stride=2)
        ### Upsampling
        self.ucc3=self.UCC(first_ch*8,first_ch*4)
        self.ucc2=self.UCC(first_ch*4,first_ch*2)
        self.ucc1=self.UCC(first_ch*2,first_ch*1)
        ### out layer
        self.out=nn.Conv2d(first_ch,out_ch,1)

    def forward(self,x):
        x=self.cinput1(x)
        x=self.cinput2(x)
        inx=[x]
        x=self.dcc1(x)
        inx.append(x)
        
        x=self.dcc2(x)
        inx.append(x)
        
        x=self.dcc3(x)
        inx.append(x)
        
        inx=inx[::-1]
        inx=inx[1:]
        
        def link(x,y):
            ncrop=(y.shape[2] - x.shape[2])//2 
            x = torch.cat([y[:,:,ncrop:-ncrop,ncrop:-ncrop],x],dim=1)
            return x
        
        
        x=self.u3(x)
        x=link(x,inx[0])
        x=self.ucc3(x)
        
        x=self.u2(x)
        x=link(x,inx[1])
        x=self.ucc2(x)
        
        x=self.u1(x)
        x=link(x,inx[2])
        x=self.ucc1(x)
        
        x=self.out(x)
        
        return x