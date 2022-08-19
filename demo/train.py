#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   train.py
@Time    :   2022/08/08 14:22:30
@Author  :   Weng Jiangwei 
@Github :    https://github.com/wengjiangwei
@Desc    :   
# send the training report to email
python train.py  --model_config ../demo/configs.yaml  --email_config ../demo/email_config.yaml  
            # Not send the training report to email
python train.py  --model_config ../demo/configs.yaml
# or  debug mode -> 
        import train; train.run(model_config = r'../demo/configs.yaml',email_config = r'../email_config.yaml')
'''


import os
import sys
from tkinter import E
module_dir = os.path.abspath(os.path.join(os.getcwd(), "../.."))
sys.path.insert(0, module_dir)
print(sys.path)
import yaml
import argparse
import re
from Honey.tools.DatasetUtils import convert2tempDatafolder
from Honey.libs.det_module.yolov5_v6 import train as yolov5_train
from Honey.tools.ReportUtils import TrainReport_yolov5
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
        with open(opt.model_config,'r') as f:
            yaml_data = yaml.load(f,Loader=yaml.FullLoader)

        data = yaml_data['data']
        if not os.path.exists(yaml_data['project_path']):
            os.makedirs(yaml_data['project_path'])

        if not os.path.exists(data):
            convert2tempDatafolder(yaml_data['root_path'], yaml_data['anno_path'], yaml_data['class_name'], yaml_data['train_val_prec'])

        yolov5_train.run(**yaml_data)

        #report the results
        SAVE_PROJECT_PATH = report_max_idx(yaml_data['project_path'],yaml_data['name'])
        SVAE_PDF_PATH = yaml_data['PDF_path']
        PROJECT_INFOR = [yaml_data['project_version'],yaml_data['developer']]
        res = TrainReport_yolov5(SAVE_PROJECT_PATH,SVAE_PDF_PATH)
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
    parser.add_argument('--model_config','--mconfig', type=str, help='initial filt path')
    parser.add_argument('--email_config','--econfig', type=str, default=None, help='initial filt path')
    return parser.parse_known_args()[0] if known else parser.parse_args()

def run(**kwargs):
    # Usage: import train; train.run(model_config = r'../demo/configs.yaml',email_config = r'../email_config.yaml')

    opt = parse_opt(True)
    for k, v in kwargs.items():
        setattr(opt, k, v)
    main(opt)

    return opt

if __name__ == '__main__':

    opt = parse_opt()
    main(opt)


    # run(model_config = r'/home/wjw/Work/Honey/demo/configs.yaml',email_config = r'/home/wjw/email_config.yaml')
    ...
