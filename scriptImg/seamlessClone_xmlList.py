# 注意修改路径！
import cv2,os
import numpy as np
import xml.etree.ElementTree as ET
from JoTools.txkjRes.deteRes import DeteRes
from  PIL import Image
from tqdm import tqdm




if __name__=="__main__":
    # Read images : src image will be cloned into dst
    ## 背景图所在文件夹
    img_dir = r'E:\Data\Temp\fake\source'
    ## 合成后的结果图所在文件夹
    output_dir = r'E:\Data\Temp\fake\save'
    os.makedirs(output_dir,exist_ok=True)

    ## 是否依据标注框进行resize,推荐 is_resize = True
    is_resize = True
    # 素材obj_crop所在文件夹，xml所标注的label 即 图片名
    obj_base_dir = r'E:\Data\Temp\fake\target'

    # 标注xml所在文件夹
    xml_dir = r'E:\Data\Temp\fake\source'

    img_list = [p for p in os.listdir(img_dir) if p.endswith('.jpg') or p.endswith('.JPG') ]
    xml_list = [p for p in os.listdir(xml_dir) if p.endswith('.xml')]

    for img_name in tqdm(img_list):
        img_path = os.path.join(img_dir,img_name)
        im = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), 1)
        file_main,extension = os.path.splitext(img_name)

        xml_name = file_main + '.xml'
        if xml_name in xml_list:
            xml_path = os.path.join(xml_dir,xml_name)
            dete_res = DeteRes(xml_path=xml_path, assign_img_path=img_path)
            for i,dete_obj in  enumerate(dete_res.alarms):
                label, xmin, ymin, xmax, ymax = dete_obj.tag, dete_obj.x1, dete_obj.y1, dete_obj.x2, dete_obj.y2
                x_center = int((xmax + xmin) / 2)
                y_center = int((ymax + ymin) / 2)
                obj_crop_path = os.path.join(obj_base_dir,(label+'.jpg'))
                obj = cv2.imdecode(np.fromfile(obj_crop_path, dtype=np.uint8), 1)
                if is_resize:
                    obj = cv2.resize(obj, (int(xmax-xmin), int(ymax-ymin)))

                # Create an all white mask
                mask = 255 * np.ones(obj.shape, obj.dtype)
                # The location of the center of the src in the dst
                width, height, channels = im.shape
                center = (x_center,y_center)
                # Seamlessly clone src into dst and put the results in output
                normal_clone = cv2.seamlessClone(obj, im, mask, center, cv2.NORMAL_CLONE)

                save_path = os.path.join(output_dir, file_main+'_+_'+str(i)+'.jpg')
                xml_save_path =  os.path.join(output_dir, file_main+'_+_'+str(i)+'.xml')

                ## 一个obj_crop目标生成一张图
                cv2.imencode('.jpg', normal_clone)[1].tofile(save_path)

                # 生成标注xml
                dete_res_= dete_res.filter_by_tags(need_tag=[label],update=False)
                # dete_res_.update_tags({label:'hole'})  # 可转换label
                dete_res_.save_to_xml(xml_save_path)






