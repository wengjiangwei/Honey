#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   gene_dataset.py
@Time    :   2022/07/29 15:11:52
@Author  :   Weng Jiangwei 
@Version :   0.0
@Contact :   wengjiangwei@tuxingkeji.com
@Desc    :   None

#FOR yolov5
'''

# here put the import lib
import os
import shutil
import yaml

import os
import random
import xml.etree.ElementTree as ET
import pickle
import os
import yaml

def convert(size, box):
        dw = 1. / size[0]
        dh = 1. / size[1]
        x = (box[0] + box[1]) / 2.0
        y = (box[2] + box[3]) / 2.0
        w = box[1] - box[0]
        h = box[3] - box[2]
        x = x * dw
        w = w * dw
        y = y * dh
        h = h * dh
        return (x, y, w, h)

def convert_annotation(image_id,DETECT_CLASS):
        in_file = open(SAVE_PATH+'/Annotations/%s.xml' % (image_id), 'r', encoding="UTF-8")
        out_file = open(SAVE_PATH+'/labels/%s.txt' % (image_id), 'w')
        tree = ET.parse(in_file)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)
    
        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            cls = obj.find('name').text
            if cls not in DETECT_CLASS or int(difficult) == 1:
                continue
            cls_id = DETECT_CLASS.index(cls)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
                float(xmlbox.find('ymax').text))
            bb = convert((w, h), b)
            out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


def spilt_dataset_coco(XML_PATH,TRAIN_VAL_PRECE,DATASET_CLASS,DETECT_CLASS):
    total_xml = os.listdir(XML_PATH)
    num = len(total_xml)
    list = range(num)
    tv = int(num * TRAIN_VAL_PRECE)
    trainval = random.sample(list, tv)
    
    ftrain = open(SAVE_PATH+'/ImageSets/train.txt', 'w')
    fval = open(SAVE_PATH+'/ImageSets/val.txt', 'w')
    
    for i in list:
        name = total_xml[i][:-4] + '\n'
        if i in trainval:
            fval.write(name)
        else:
            ftrain.write(name)
    ftrain.close()
    fval.close()

    for image_set in DATASET_CLASS:
        if not os.path.exists(SAVE_PATH+'/labels/'):
            os.makedirs(SAVE_PATH+'/labels/')
        image_ids = open(SAVE_PATH+'/ImageSets/%s.txt' % (image_set)).read().strip().split()
        list_file = open(SAVE_PATH+'/%s.txt' % (image_set), 'w')
        for image_id in image_ids:
            list_file.write(SAVE_PATH+'/images/%s.jpg\n' % (image_id))#
            convert_annotation(image_id,DETECT_CLASS)
        list_file.close()


def template_dataset(ROOT_PATH,SAVE_PATH,CLASS_NAME,TRAIN_VAL_PRECE=None):

    if not os.path.exists(SAVE_PATH):
        file_set =['Annotations','images','ImageSets','JPEGImages']
        for file_name in file_set:
            os.makedirs(SAVE_PATH+"/"+file_name)
    
    img_set = []
    for img_name in os.listdir(ROOT_PATH):
        if os.path.splitext(img_name)[1]=='.jpg':
            img_set.append(img_name)
    for img_name in img_set: 
        shutil.copyfile(ROOT_PATH+"/"+img_name,SAVE_PATH+'/images/'+img_name)
        shutil.copyfile(ROOT_PATH+"/"+img_name,SAVE_PATH+'/JPEGImages/'+img_name)

    xml_set = []
    for xml_name in os.listdir(ROOT_PATH):
        if os.path.splitext(xml_name)[1]=='.xml':
            xml_set.append(xml_name)
    for xml_name in xml_set: 
        shutil.copyfile(ROOT_PATH+"/"+xml_name,SAVE_PATH+'/Annotations/'+xml_name)

    DATASET_CLASS = ['train','val']
    XML_PATH = SAVE_PATH+'/Annotations/'
    if TRAIN_VAL_PRECE  is not None:
        spilt_dataset_coco(XML_PATH,TRAIN_VAL_PRECE,DATASET_CLASS,CLASS_NAME)

    desired_caps = {
    'train':SAVE_PATH+"/val.txt",
    'val':SAVE_PATH+"/val.txt",
    'nc':len(CLASS_NAME),
    'names':CLASS_NAME,
                    }

    with open(SAVE_PATH+'/data.yaml','w',encoding="utf-8") as f:
        yaml.dump(desired_caps,f)

if __name__ == '__main__':

    ROOT_PATH = r"/home/wjw/Work/Data/A_Rawdata/ft_AutoXML_729"
    CLASS_NAME = ["ftqx",'ljdl']
    SAVE_PATH = r"/home/wjw/Work/Data/ft_AutoXML_729"

    template_dataset(ROOT_PATH,SAVE_PATH,CLASS_NAME,TRAIN_VAL_PRECE=0.1)

    # SAVE_PATH = '/home/wjw/Work/Data/ft'
    # TRAIN_VAL_PRECE = 0.1
    # DATASET_CLASS = ['train','val']
    # DETECT_CLASS = ["ftqx",'ljdl']
    # XML_PATH = 'Annotations'
    # spilt_dataset_coco(SAVE_PATH,TRAIN_VAL_PRECE,DATASET_CLASS,DETECT_CLASS,XML_PATH)


