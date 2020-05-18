# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 16:31:51 2020

@author: Jasmine
"""

import os
import sys
import numpy as np
#import matplotlib.pyplot as plt
import torch
from torch.utils.data import Dataset, DataLoader
from sklearn.metrics import roc_curve,auc
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
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
    
def test_unet(unet,dataloader) :
    results=[]
    for sample in dataloader:
        I=sample['image']
        J=sample['label']
        Jhat=unet(I)
        ncrop=(J.shape[2]-Jhat.shape[2])//2
        Jc=J[:,ncrop:-ncrop,ncrop:-ncrop]
        Ic = I[:,:,ncrop:-ncrop,ncrop:-ncrop]
        for i in range(len(Ic)):
            origin=np.transpose(Ic[i].numpy().astype(np.uint8),[1,2,0])
            label=Jc[i].numpy()
            prob=torch.softmax(Jhat.detach(),dim=1)[i,1].numpy()
            sample={'o':origin,'l':label,'p':prob}
            results.append(sample)
    return results

def extend_pixels(results):
    y=[]
    yhat=[]
    for i in results:
        label=i['l']
        prob=i['p']
        label_list=(label.reshape((1,-1))).tolist()[0]
        prob_list=(prob.reshape((1,-1))).tolist()[0]
        y.extend(label_list)
        yhat.extend(prob_list)
    return y,yhat 


# =============================================================================
# def draw_auc(fpr,tpr,roc_auc,output_path):
#     plt.figure()
#     plt.plot(fpr,tpr,color="darkorange",
#              lw=2,label="ROC curve (Area = %0.2f)" % roc_auc)
#     plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
#     plt.xlim([0.0, 1.0])
#     plt.ylim([0.0, 1.05])
#     plt.xlabel('False Positive Rate')
#     plt.ylabel('True Positive Rate')
#     plt.title('Receiver operating characteristic example')
#     plt.legend(loc="lower right")
#     plt.savefig(os.path.join(output_path,'ROC.png'))
# =============================================================================

# =============================================================================
# nshow=100
# for i in range(nshow):
#     sample=results[i]
#     origin=sample['o']
#     label=sample['l']
#     prob=sample['p']
#     print(np.max(label))
#     print(np.min(label))
#     plt.figure(i)
#     plt.subplot(131)
#     plt.imshow(origin)
#     plt.subplot(132)
#     plt.imshow(label)
#     plt.subplot(133)
#     plt.imshow(prob,vmin=0,vmax=1)
#     plt.show() 
# =============================================================================
    
def main(argv):
    Testset_path=argv[0]  # path to training dataset
    input_path=argv[1]
    unet = UNet(in_ch=3, # number of channels in input image, RGB=3
            out_ch=2, # number of channels in output image, classification here is forground or background=2
            first_ch=8, # how many features at the first layer
            nmin=9, # minimum image size, this will define how big our input images need to be (it is printed)
           )
    unet.load_state_dict(torch.load(input_path))
    AD_DataSet=ADdataset(path=Testset_path,transform=ToTensor())
    AD_DataLoader=DataLoader(AD_DataSet,batch_size=1,shuffle=False,num_workers=0)
    print("The unet architecture:",unet)
    print("esting....")
    results=test_unet(unet=unet,
                    dataloader=AD_DataLoader)
    
    print("Finished testing, start evaluating...")
    y,yhat=extend_pixels(results)
    fpr,tpr,threshold=roc_curve(y,yhat)
    roc_auc=auc(fpr,tpr)
    optimal_idx = np.argmax(tpr - fpr)
    optimal_threshold = threshold[optimal_idx]
    optimal_yhat=list(map(int,(yhat>=optimal_threshold).tolist()))
    Confusion_matrix = confusion_matrix(y, optimal_yhat) 
    print('AUC:',roc_auc)
    print('Optimal_threshold:',optimal_threshold)
    print ('Confusion Matrix :')
    print(Confusion_matrix) 
    print ('Optimal Accuracy :',accuracy_score(y, optimal_yhat))
    #draw_auc(fpr,tpr,roc_auc,output_path)

  
if __name__ == '__main__':
    main(sys.argv[1:])