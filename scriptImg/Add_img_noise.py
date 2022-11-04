# -*- coding: utf-8 -*-

import cv2
import numpy as np
import os.path
import shutil
import random

# 椒盐噪声
def SaltAndPepper(src, percetage):
    SP_NoiseImg = src.copy()
    SP_NoiseNum = int(percetage * src.shape[0] * src.shape[1])
    for i in range(SP_NoiseNum):
        randR = np.random.randint(0, src.shape[0] - 1)
        randG = np.random.randint(0, src.shape[1] - 1)
        randB = np.random.randint(0, 3)
        if np.random.randint(0, 1) == 0:
            SP_NoiseImg[randR, randG, randB] = 0
        else:
            SP_NoiseImg[randR, randG, randB] = 255
    return SP_NoiseImg


# 高斯噪声
def addGaussianNoise(image, percetage):
    G_Noiseimg = image.copy()
    w = image.shape[1]
    h = image.shape[0]
    G_NoiseNum = int(percetage * image.shape[0] * image.shape[1])
    for i in range(G_NoiseNum):
        temp_x = np.random.randint(0, h)
        temp_y = np.random.randint(0, w)
        G_Noiseimg[temp_x][temp_y][np.random.randint(3)] = np.random.randn(1)[0]
    return G_Noiseimg


def brightness(img,gamma):#gamma大于1时图片变暗，小于1图片变亮
	#具体做法先归一化到1，然后gamma作为指数值求出新的像素值再还原
	gamma_table = [np.power(x/255.0,gamma)*255.0 for x in range(256)]
	gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)
	#实现映射用的是Opencv的查表函数
	return cv2.LUT(img,gamma_table)



if __name__ == '__main__':
    # 图片文件夹路径
    input_jpg = r'E:\Data\Temp\fake\all_imgs_aug'
    input_xml = r'E:\Data\Temp\fake\all_xml_aug'
    output_jpg = r'E:\Data\Temp\fake\all_imgs_noise'
    output_xml = r'E:\Data\Temp\fake\all_xml_noise'
    if not os.path.exists(output_jpg):
        os.makedirs(output_jpg)
    if not os.path.exists(output_xml):
        os.makedirs(output_xml)       

    for img_name in os.listdir(input_jpg):
        name = img_name.split('.')[0]
        # print(name)
        # print(img_name)
        img_path = os.path.join(input_jpg, img_name)
        img = cv2.imread(img_path)
        try:
            xml_src_path = os.path.join(input_xml, name + '.xml')
            xml_dst_path = os.path.join(output_xml, name)
            if bool(random.getrandbits(1)):
            # 增加噪声
                # img_gauss = addGaussianNoise(img, 0.3)
                # cv2.imwrite(os.path.join(output_jpg, name + '_noise.jpg'), img_gauss)
                # shutil.copyfile(xml_src_path, xml_dst_path + '_noise.xml')
                # print("Save " + os.path.join(output_jpg, name + '_noise.jpg') + " Successfully!")
                
                # 变亮
                
                img_darker = brightness(img,random.randint(4,9)/10)
                cv2.imwrite(os.path.join(output_jpg, name + '_darker.jpg'), img_darker)
                shutil.copyfile(xml_src_path, xml_dst_path + '_darker.xml')
                # print("Save " + os.path.join(output_jpg, name + '_darker.jpg') + " Successfully!")
            else:
                # 变暗
                img_brighter = brightness(img,random.randint(1,2))
                cv2.imwrite(os.path.join(output_jpg, name + '_brighter.jpg'), img_brighter)
                shutil.copyfile(xml_src_path, xml_dst_path + '_brighter.xml')
                # print("Save " + os.path.join(output_jpg, name + '_brighter.jpg') + " Successfully!")

                # blur = cv2.GaussianBlur(img, (7, 7), 3)
                # #      cv2.GaussianBlur(图像，卷积核，标准差）
                # cv2.imwrite(os.path.join(output_jpg, name + '_blur.jpg'), blur)
                # shutil.copyfile(xml_src_path, xml_dst_path + '_blur.xml')
                # print("Save " + os.path.join(output_jpg, name + '_blur.jpg') + " Successfully!")
        except:
            continue
