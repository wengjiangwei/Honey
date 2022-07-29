#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test.py
@Time    :   2022/07/11 19:14:18
@Author  :   Weng Jiangwei 
@Version :   0.0
@Contact :   wengjiangwei@tuxingkeji.com
@Desc    :   None
'''

# here put the import lib

import torch
from torchvision import datasets, models, transforms
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import time
import numpy as np
import matplotlib.pyplot as plt
import models


# -*- coding:utf-8 -*-
# @time : 2019.12.02
# @IDE : pycharm
# @author : wangzhebufangqi
# @github : https://github.com/wangzhebufangqi

#数据集的类别
NUM_CLASSES = 2

#训练时batch的大小
BATCH_SIZE = 32

#训练轮数
NUM_EPOCHS= 25

##预训练模型的存放位置
#下载地址：https://download.pytorch.org/models/resnet50-19c8e357.pth
PRETRAINED_MODEL = './resnet50-19c8e357.pth'

##训练完成，权重文件的保存路径,默认保存在trained_models下
TRAINED_MODEL = 'trained_models/vehicle-10_record.pth'

#数据集的存放位置
TRAIN_DATASET_DIR = './snlf/train'
VALID_DATASET_DIR = './snlf/val'



def run(path,datasets):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")#若有gpu可用则用gpu
    test_valid_transforms = transforms.Compose(
            [transforms.ToPILImage(),
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406],
            [0.229, 0.224, 0.225])])

    model = models.resnet50()
    fc_inputs = model.fc.in_features
    model.fc = nn.Sequential(
        nn.Linear(fc_inputs, 256),
        nn.ReLU(),
        nn.Dropout(0.4),
        nn.Linear(256, 2),
        nn.LogSoftmax(dim=1)
    )

    model.load_state_dict(torch.load(path),strict=False)
    model = model.to(device)

    for inputs in datasets:
        with torch.no_grad():
            model.eval()#验证
            inputs = test_valid_transforms(inputs).unsqueeze(0)
            inputs = inputs.to(device)
            
            outputs = model(inputs)
            ret, predictions = torch.max(outputs.data, 1)
    return predictions


if __name__=='__main__':
    import os
    import cv2
    path_all = os.listdir('/home/wjw/Data/gtzt/test_img/')
    data =[]
    for path in path_all:
        data.append(cv2.imread('/home/wjw/Data/gtzt/test_img/'+path))
    predictions = run('/home/wjw/Suanfa2_crack_dect/lib/classification/resnet50-19c8e357.pth',\
        data)
    print(predictions)