# -*- coding: utf-8  -*-
# -*- author: jokker -*-


from JoTools.operateDeteRes import OperateDeteRes
import os

xml_dir = r"E:\Data\Temp\2022_10_27安监苗雨\crop_2"
region_img_dir = r"E:\Data\Temp\2022_10_27安监苗雨\10_22_img"
save_xml_dir = r"E:\Data\Temp\2022_10_27安监苗雨\annotations_new_1101"

if not os.path.exists(save_xml_dir):
    os.mkdir(save_xml_dir)

OperateDeteRes.get_xml_from_crop_img(crop_dir=xml_dir, region_img_dir=region_img_dir, save_xml_dir=save_xml_dir)
