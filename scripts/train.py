#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   train.py
@Time    :   2022/08/08 14:22:30
@Author  :   Weng Jiangwei 
@Github :    https://github.com/wengjiangwei
@Desc    :   None
'''

import os
import sys
sys.path.append(r'/home/wjw/Work')# Honey path
import configparser
import argparse
from Honey.tools import DatasetUtils
from Honey.libs.det_module.yolov5_v6 import train as yolov5_train




def main(opt):  # sourcery skip: move-assign
    config = configparser.ConfigParser()
    config = config.read(opt.ini_filename)
    root_path = "/home/wjw/Work/Data/A_Rawdata/ft_AutoXML_729"
    class_name = ["ftqx", 'ljdl']
    save_path = "/home/wjw/Work/Data/ft_AutoXML_729"
    data = os.path.join(save_path,'data.yaml')  # 数据yaml文件
    weights = '/home/wjw/Work/Weights/YOLOV5/yolov5l.pt'  # 预训练权重
    cfg = '/home/wjw/Work/Honey/libs/det_module/yolov5_v6/models/yolov5l.yaml'  # 模型结构
    hyp = '/home/wjw/Work/Honey/libs/det_module/yolov5_v6/data/hyps/hyp.scratch-low.yaml'  # 其余超参数（yaml文件）
    input_path = '/home/wjw/Work/Runs/v5-ft'  # 保存路径

    # epochs = 200#迭代次数
    batch_size = 8  # 每次送入的图片
    # hyp = #其余超参数（yaml文件）
    if not os.path.exists(data):
        DatasetUtils(root_path, save_path, class_name, TRAIN_VAL_PRECE=0.1)

    yolov5_train.run(ROOT=input_path, data=data, weights=weights, cfg=cfg,
                    hyp=hyp, project=input_path, batch_size=batch_size)


def parse_opt(known=False):
    parser = argparse.ArgumentParser()
    parser.add_argument('--config_path', type=str, help='initial filt path')
    return parser.parse_known_args()[0] if known else parser.parse_args()

def run(**kwargs):
    # Usage: import train; train.run(data='coco128.yaml', imgsz=320, weights='yolov5m.pt')
    ROOT = ROOT
    opt = parse_opt(True)
    for k, v in kwargs.items():
        setattr(opt, k, v)
    main(opt)
    return opt




