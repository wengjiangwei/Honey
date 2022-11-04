#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   crop_img_copy.py
@Time    :   2022/08/16 10:05:10
@Author  :   Weng Jiangwei 
@Github :    https://github.com/wengjiangwei
@Desc    :   None
'''


import shutil
import os
from tqdm import tqdm
xml_path = r'E:\Data\避雷器缺护罩\crop_xml'
root_path = r'E:\Data\避雷器缺护罩\JPEGImages'
xml_names = os.listdir(xml_path)
for xml_name in tqdm(xml_names):
    name = os.path.splitext(xml_name)[0]
    # img_name = os.path.join(root_path, name+'.jpg')
    img_name = os.path.join(root_path, name+'.JPG')
    shutil.copy(img_name,xml_path)