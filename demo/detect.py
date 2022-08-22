#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   det_demo.py
@Time    :   2022/07/11 19:01:44
@Author  :   Weng Jiangwei 
@Version :   0.0
@Contact :   wengjiangwei@tuxingkeji.com
@Desc    :   None
'''
import os
import sys
from tkinter import E
sys.path.append(r'/home/wjw/Work')# Honey path
import yaml
import argparse
import re
from Honey.tools import DatasetUtils
from Honey.libs.det_module.yolov5_v6 import detect as yolov5_detect
from Honey.tools.ReportUtils import DetectReport_yolov5
from Honey.utils.EmailUtils import config2email,config2email_error
from Honey.utils.common import report_max_idx
import traceback

#TODO: YOLOV5  --- other model

def main(opt:argparse): 
    """train the yolov5 with yaml settings file
    Parameters
    ----------
    opt : argparse
        add_argument in the terminal format
    """    
    try:
        with open(opt.config_path,'r') as f:
            yaml_data = yaml.load(f,Loader=yaml.FullLoader)

        data = os.path.join(yaml_data['project'],yaml_data['name'])
        if not os.path.exists(data):
            os.makedirs(data)

        PROJECT_VERSION = yaml_data['project_version']
        DEVELOPER = yaml_data['developer']
        PDF_PATH = yaml_data['PDF_path']
        GT_XML_ROOT = yaml_data['gt_xml_root']
        TARGET = yaml_data['target']
        IOU_THERSHOLD = yaml_data['iou_thres']
        pop_list = ['project_version','developer','PDF_path','gt_xml_root','target']
        for pop_i in pop_list:
            yaml_data.pop(pop_i)


        yolov5_detect.run(**yaml_data)

        # report the results
        SAVE_PROJECT_PATH = report_max_idx(yaml_data['project'],yaml_data['name'])
        PROJECT_INFOR = [PROJECT_VERSION,DEVELOPER]
        SVAE_PDF_PATH = PDF_PATH
        GT_XML_ROOT = GT_XML_ROOT
        TARGET = TARGET
        IOU_THERSHOLD = IOU_THERSHOLD
        res = DetectReport_yolov5(SAVE_PROJECT_PATH,SVAE_PDF_PATH,GT_XML_ROOT,TARGET,IOU_THERSHOLD)
        email_attachment = res.write(PROJECT_INFOR)
        # send email
        if opt.email_config is not None: 
            config2email(opt.email_config,email_attachment)

    except:
        print(traceback.format_exc())
        # send error email
        # if opt.email_config is not None: # send email
        #     config2email_error(opt.email_config,traceback.format_exc())

def parse_opt(known=False):
    # argparse in terminal
    parser = argparse.ArgumentParser()
    parser.add_argument('--config_path', type=str, help='detect filt path')
    parser.add_argument('--email_config', type=str, default=None, help='initial filt path')
    return parser.parse_known_args()[0] if known else parser.parse_args()

def run(**kwargs):
    # Usage: import train; train.run(config_path = r'../demo/detect.yaml',email_config = r'../email_config.yaml')

    opt = parse_opt(True)
    for k, v in kwargs.items():
        setattr(opt, k, v)
    main(opt)

    return opt


if __name__ == '__main__':

    # opt = parse_opt()
    # main(opt)

    run(config_path=r'/home/wjw/Work/Honey/demo/detect.yaml', email_config=r'/home/wjw/Work/Honey/email_config.yaml')

    


