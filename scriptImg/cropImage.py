from JoTools.operateDeteRes import OperateDeteRes
from JoTools.utils.FileOperationUtil import FileOperationUtil
from JoTools.txkjRes.deteRes import DeteRes
import os
import argparse


img_dir = r"E:\Data\Temp\2022_10_27安监苗雨\10_22_img"
xml_dir = r"E:\Data\Temp\2022_10_27安监苗雨\10_22_img"
save_dir = r"E:\Data\Temp\2022_10_27安监苗雨\crop_2"
augment_parameter = [0.1,0.1,0.1,0.1]

if not os.path.exists(save_dir):
    os.mkdir(save_dir)

def parse_args():
    parser = argparse.ArgumentParser(description='Tensorflow Faster R-CNN demo')
    parser.add_argument('--img', dest='img', type=str, default=img_dir)#图片路径
    parser.add_argument('--xml', dest='xml', type=str, default=xml_dir)#xml路径
    parser.add_argument('--save', dest='save', type=str, default=save_dir)#保存路径

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    img_dir = args.img
    xml_dir = args.xml
    save_dir = args.save

    OperateDeteRes.crop_imgs(img_dir=img_dir, xml_dir=xml_dir, save_dir=save_dir, split_by_tag=True, augment_parameter=None)
    # OperateDeteRes.crop_imgs_angles(img_dir=img_dir, xml_dir=xml_dir, save_dir=save_dir, split_by_tag=True, augment_parameter=None)

