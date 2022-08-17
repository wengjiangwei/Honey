#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   DatasetUtils.py
@Time    :   2022/08/05 15:21:46
@Author  :   Weng Jiangwei 
@Github :    https://github.com/wengjiangwei
@Desc    :   To convert dataset formats for YOLOv5 in windows and Linux environments.
'''

# from asyncio.log import logger
from logging import warning
import os
import shutil
from tkinter import E
import yaml
import random
import xml.etree.ElementTree as ET
from tqdm import tqdm
def _convert(size:list, box:list)->list:

    """convert the size of image to the normalized value of the box
    Note that: 

    Args:
        size (list): (width, height) of image
        box (list): (xmin,xmax,ymin,ymax) of box

    Returns:
        list: (x_center, y_center, width, height) of the normalized value
    
    """    
    dw = 1. / size[0]
    dh = 1. / size[1]
    #TODO：check (x,y,width,height) 
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

def convert_annotation(save_path:str,image_id:str,det_class:list)->None:

    """Read a save_path XML file and convert it into a txt file
    Note that: Need "convert" function to convert, included.

    Args:
        save_path (str): the root folder of the save_path (annotations & label,etc.)
        image_id (str): the index of the image file
        det_class (list): the class of the detected objects
    Return:
        None
    """   
    in_file = open(os.path.join(save_path,'Annotations','%s.xml' % (image_id)),'r',encoding="UTF-8")
    out_file = open(os.path.join(save_path,'labels','%s.txt' % (image_id)), 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    try:
        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            cls = obj.find('name').text
            if cls not in det_class or int(difficult) == 1:
                continue
            cls_id = det_class.index(cls)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
                float(xmlbox.find('ymax').text))
            bb = _convert((w, h), b)
            out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
    except:
        pass
        # logger.error("Failed to convert xml, dut to the wrong structured format.",exc_info=True)

def _spilt_dataset_coco(save_path:str,train_val_prece:float,det_class:list,dataset_name:list=['train','val'])->None:
    """template for generating dataset_coco format
    Split dataset into train and val txt files and labels files.

    Args:
        save_path (str): the root folder of the save_path (annotations & label,etc.)
        train_val_prece (float): the ratio of the training and validation datasets
        det_class (list): detection objects for classification
        dataset_name (list, optional): _description_. Defaults to ['train','val'].
    """
    total_xml = os.listdir(os.path.join(save_path,'Annotations'))
    num = len(total_xml)
    list = range(num)
    tv = int(num * train_val_prece)
    trainval = random.sample(list, tv)
    
    ftrain = open(os.path.join(save_path,'ImageSets','train.txt'), 'w')
    fval = open(os.path.join(save_path,'ImageSets','val.txt'), 'w')
    
    for i in list:
        name = total_xml[i][:-4] + '\n'
        if i in trainval:
            fval.write(name)
        else:
            ftrain.write(name)
    ftrain.close()
    fval.close()

    for image_set in dataset_name:
        if not os.path.exists(os.path.join(save_path,'labels')):
            os.makedirs(os.path.join(save_path,'labels'))
        image_ids = open(os.path.join(save_path,'ImageSets','%s.txt' % (image_set))).read().strip().split()
        list_file = open(os.path.join(save_path,'%s.txt' % (image_set)), 'w')
        _image_temp = os.listdir(os.path.join(save_path,"JPEGImages"))
        image_type = os.path.splitext(_image_temp[0])[1]
        for image_id in tqdm(image_ids,desc=f'converting annotations in {image_set}'):
            #TODO: add image type: JPG/jpg/jpeg etc...
            if image_type == '.jpg':
                list_file.write(os.path.join(save_path,'images','%s.jpg\n' % (image_id)))#
                _convert_annotation(save_path,image_id,det_class)
            elif image_type == '.JPG':
                list_file.write(os.path.join(save_path,'images','%s.JPG\n' % (image_id)))#
                _convert_annotation(save_path,image_id,det_class)
            else:
                print("unknown image type!")
        list_file.close()

def convert2tempDatafolder(root_path:str,save_path:str,class_name:list,train_val_prece:float=0.2)->None:
    """convert2tempDatafolder with  dataset_coco format 
    Note that: this function is used to convert dataset from labelimg to 
    train the yolov5 (suitable model), maybe also fit other yolo-series models.
    intput: (JPG and XML files) folder
    output: (ROOT path + annotations folder, images folder, JPEGImages folder, imagesets folder, train.txt and val.txt)
    # please check JPG and jpg ！

    Args:
        root_path (str): image and XML file generated from labelimg directly.
        save_path (str): the target path that saves all sub-folders (i.e., Annotations labels & JPEGImages)
        class_name (list): select the detection class to use.
        train_val_prece (float, optional): spilt the datasets with the given ratio. Defaults to 0.2.
    """

    warning("CHECK: target annotation axis is (x,y,width,height)")
    warning(f"CHECK: train_val_prece is {train_val_prece}")
    if not os.path.exists(save_path):
        file_set =['Annotations','images','ImageSets','JPEGImages']
        for file_name in file_set:
            os.makedirs(os.path.join(save_path,file_name))
    
    img_set = []
    xml_set = []
    #TODO: add image type: JPG/jpg/jpeg etc...
    for img_name in os.listdir(root_path):
        if os.path.splitext(img_name)[1]=='.jpg' or os.path.splitext(img_name)[1]== ".JPG":
            img_set.append(img_name)
        elif os.path.splitext(img_name)[1]=='.xml':
            xml_set.append(img_name)
        else:
            warning("Unknown formats!")

    for img_name in tqdm(img_set,desc='Images copying'): 
        shutil.copyfile(os.path.join(root_path,img_name),os.path.join(save_path,'images',img_name),)
        shutil.copyfile(os.path.join(root_path,img_name),os.path.join(save_path,'JPEGImages',img_name))

    for xml_name in tqdm(xml_set,desc='XMLs copying'): 
        shutil.copyfile(os.path.join(root_path,xml_name),os.path.join(save_path,'Annotations',xml_name))

    if train_val_prece is not None:
        _spilt_dataset_coco(save_path,train_val_prece,class_name)

    desired_caps = {
    'train':os.path.join(save_path,"train.txt"),
    'val':os.path.join(save_path,"val.txt"),
    'nc':len(class_name),
    'names':class_name,
                    }

    with open(os.path.join(save_path,'data.yaml'),'w',encoding="utf-8") as f:
        yaml.dump(desired_caps,f)

if __name__ == '__main__':

    ROOT_PATH = ...
    SAVE_PATH = ...
    CLASS_NAME = ...
    # train_val_prece = 0.1 
    convert2tempDatafolder(ROOT_PATH,SAVE_PATH,CLASS_NAME)



