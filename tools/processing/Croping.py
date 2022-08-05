from email.header import Header
from turtle import width

# !/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Croping.py
@Time    :   2022/07/11 09:49:45
@Author  :   Weng Jiangwei 
@Version :   0.0
@Contact :   wengjiangwei@tuxingkeji.com
@Desc    :   Image croping
'''

# here put the import lib
import os
import cv2


class Croping:
    ''' '''

    def __init__(self, img_path, crop_size, step):
        self.img_path = img_path
        self.crop_size = crop_size
        self.step = step
        try:
            self.img = cv2.imread(img_path)
        except:
            self.img = self.img_path
        self.width, self.height, self.channel = self.img.shape
        self.crop_all = []

    def transformer(self):
        if self.crop_size > self.width or self.crop_size > self.height:
            assert ("self.crop_size>self.width or self.crop_size>self.height")

        self.x = 0
        while ((self.x + self.crop_size) <= self.width):
            self.y = 0
            while ((self.y + self.crop_size) <= self.height):
                sub_img = self.img[self.x:self.x + self.crop_size, self.y:self.y + self.crop_size, :]
                self.crop_all.append([self.x, self.y, sub_img])
                self.y = self.y + self.step
            self.x = self.x + self.step

        return self.crop_all

    def transformer_save(self, save_path):
        self.crop_all = self.transformer()
        (filepath, tempfilename) = os.path.split(self.img_path)
        (filename, extension) = os.path.splitext(tempfilename)
        for x, y, img in self.crop_all:
            cv2.imwrite(os.path.join(save_path, str(filename) + "_" + str(x) + "_" + str(y) + '.jpg'), img)


if __name__ == '__main__':

    ROOT_PATH = "/home/wjw/Data/auto_detect_lf/Images/exp2/crops/gtzt/"
    save_path = '/home/wjw/Data/auto_detect_lf/crop'
    files = os.listdir(ROOT_PATH)
    for img_path in files:
        img_path = '/home/wjw/Data/auto_detect_lf/Images/exp2/crops/gtzt/' + img_path
        crop_size = 416
        step = 200
        Croping_func = Croping(img_path, crop_size, step)
        # crop_img = Croping.transformer()
        Croping_func.transformer_save(save_path)

