#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   train.py
@Time    :   2022/08/08 14:22:30
@Author  :   Weng Jiangwei 
@Github :    https://github.com/wengjiangwei
@Desc    :   None
'''

from __future__ import annotations
import os
import sys
from tkinter import E
sys.path.append(r'/home/wjw/Work')# Honey path
import yaml
import argparse
import re
from Honey.tools import DatasetUtils
from Honey.libs.det_module.yolov5_v6 import train as yolov5_train
from Honey.tools import ReportUtils
from Honey.utils.EmailUtils import AutoEmail,config2email

#TODO: YOLOV5  

def main(opt:argparse): 
    """train the yolov5 with yaml settings file

    Parameters
    ----------
    opt : argparse
        add_argument in the terminal format
    """    
    with open(opt.config_path,'r') as f:
        yaml_data = yaml.load(f,Loader=yaml.FullLoader)

    data = os.path.join(yaml_data['anno_path'],"data.yaml")
    if not os.path.exists(yaml_data['project_path']):
        os.makedirs(yaml_data['project_path'])

    if not os.path.exists(data):
        DatasetUtils(yaml_data['root_path'], yaml_data['anno_path'], yaml_data['class_name'], yaml_data['train_val_prec'])

    yolov5_train.run(**yaml_data)

    #report the results

    SAVE_PROJECT_PATH = report_max_idx(yaml_data['project_path'],yaml_data['name'])
    SVAE_PDF_PATH = yaml_data['PDF_path']
    PROJECT_INFOR = [yaml_data['project_version'],yaml_data['developer']]

    res = ReportUtils(SAVE_PROJECT_PATH,SVAE_PDF_PATH)
    res.write(PROJECT_INFOR)

    if opt.email_config is not None:
        config2email(opt.email_config)

def parse_opt(known=False):
    parser = argparse.ArgumentParser()
    parser.add_argument('--config_path', type=str, help='initial filt path')
    parser.add_argument('--email_config', type=str, default=None, help='initial filt path')
    return parser.parse_known_args()[0] if known else parser.parse_args()

def run_(**kwargs):
    opt = parse_opt(True)
    for k, v in kwargs.items():
        setattr(opt, k, v)
    main(opt)
    return opt

def report_max_idx(project_path, name):
    project_all = []
    project_list = os.listdir(project_path)
    for filename in project_list:
        if name in filename:
            try:
                project_idx = re.findall("\d+", filename)
                project_all.append(int(project_idx[0]))
            except Exception:
                continue
    return os.path.join(project_path, f"{name}{max(project_all)}")

if __name__ == '__main__':

    run_(config_path = r'/home/wjw/Work/Honey/demo/configs.yaml')
    # report_max_idx('/home/wjw/Work/Runs/v5-ft','ft')
    # email_config = r'/home/wjw/Work/Honey/email_config.yaml'
    # email_config = yaml.load(open(email_config), Loader=yaml.FullLoader)
    # config2email(email_config)
    ...
