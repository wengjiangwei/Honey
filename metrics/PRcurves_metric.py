import os
import xml.etree.ElementTree as ET
import shutil
import matplotlib
# matplotlib.use("Agg")
import matplotlib.pyplot as plt
from numpy import inf
import cv2
import random
from  tqdm import tqdm
class XmlUtils(object):

    def __init__(self,gt_xml_path,pr_xml_path,taget_label,iou_thershold):

        self.gt_xml_path = gt_xml_path
        self.pr_xml_path = pr_xml_path
        self.taget_label = taget_label
        self.iou_thershold = iou_thershold

    def objects_count_xml(self, xml_list, conf_thershold, gt=False):

        tot_objects = []
        for xml in xml_list:
            try:
                objects = self.xmlRead(xml)
            except Exception:
                print('----- read xml err ---->', xml)
            if len(objects) != 0:
                if not gt:
                    objects = [obj for obj in objects if obj[1] > conf_thershold]
                tot_objects.extend(objects)

        return len([obj for obj in tot_objects if obj[0] == self.taget_label])



    def xmlRead(self,xml_path):
        voc_labels = []
        tree = ET.parse(xml_path)
        root = tree.getroot()

        for obj in root.iter('object'):
            label = obj.find('name').text
            if label != self.taget_label:
                continue
            try:
                prob_ = float(obj.find('prob').text)
            except Exception:
                prob_ = 1.0
            bndbox = obj.find('bndbox')
            xmin = int(float(bndbox.find('xmin').text))
            xmax = int(float(bndbox.find('xmax').text))
            ymin = int(float(bndbox.find('ymin').text))
            ymax = int(float(bndbox.find('ymax').text))

            voc_labels.append([label, prob_, [xmin, ymin, xmax, ymax]])

        return voc_labels

    def calculate_iou(self, gt, pr):
        # xmin, ymin, xmax, ymax
        dx = max(min(gt[2], pr[2]) - max(gt[0], pr[0]) + 1, 0)
        dy = max(min(gt[3], pr[3]) - max(gt[1], pr[1]) + 1, 0)
        overlap_area = dx * dy

        union_area = (
                (gt[2] - gt[0] + 1) * (gt[3] - gt[1] + 1) +
                (pr[2] - pr[0] + 1) * (pr[3] - pr[1] + 1) -
                overlap_area
        )
        return overlap_area * 1. / union_area


    def caculate_PR(self, conf_thershold):

        common_imgs = list(set([os.path.basename(i) for i in self.gt_xml_path]) & set([os.path.basename(i) for i in self.pr_xml_path]))
        correct_inference_list = []  ## 正确目标 ##
        extra_inference_list = []  ## 多检目标 ##

        correct_num = self.objects_count_xml(self.gt_xml_path, 1, gt=True)

        total_num = self.objects_count_xml(self.pr_xml_path, conf_thershold, gt=False)

        for xml in common_imgs:
            gt_xml_dir = os.path.dirname(self.gt_xml_path[0])
            gt_xml_path = os.path.join(gt_xml_dir, xml)
            try:
                gt_objects = self.xmlRead(gt_xml_path)
            except Exception:
                print('----- read xml err ---->', os.path.join(gt_xml_dir, xml))

            pr_xml_dir = os.path.dirname(self.pr_xml_path[0])
            pr_xml_path = os.path.join(pr_xml_dir, xml)
            try:
                pr_objects = self.xmlRead(pr_xml_path)
            except Exception:
                print('----- read xml err ---->', os.path.join(pr_xml_dir, xml))

            for pr_obj in pr_objects:
                pr_label, pr_prob, pr_box = pr_obj

                for gt_obj in gt_objects:
                    gt_label, gt_prob, gt_box = gt_obj

                    ## 正确 和 多检 ##
                    if pr_label == gt_label and pr_prob > conf_thershold:

                        iou = self.calculate_iou(gt_box, pr_box)
                        if iou > self.iou_thershold:
                            correct_inference_list.append((xml, pr_box))

                        else:
                            extra_inference_list.append((xml, pr_box))

        correct_inference_num = len(correct_inference_list) if  len(correct_inference_list)<total_num else total_num

        recall = round(correct_inference_num / correct_num, 4)
        if total_num > 0:
            precision = round(correct_inference_num / total_num, 4)
        else:
            precision = recall
        print('检出目标{}'.format(total_num))
        print('应检目标{}'.format(correct_num))
        print('正确目标{}'.format(correct_inference_num))
        #print('多检{}'.format(extra_num))
        return recall, precision


    def plot_prs_PRE_F2(self, pare_listL, f2_score_list):
        fig = plt.figure()
        ax1 = fig.add_subplot(132)
        ax1.set_title(str(self.taget_label) + '----> iou_thershold=' + str(self.iou_thershold))
        ax1.set_xlabel('Recall')
        ax1.set_ylabel('Precision')
        for precision, recall, wujianbi in pare_listL:
            ax1.plot(recall, precision,label="model")
            ax1.legend(loc=0, ncol=2)
        ax2 = fig.add_subplot(133)
        ax2.set_xlabel('Recall')
        ax2.set_ylabel('ErrRate')
        for precision, recall, wujianbi in pare_listL:
            ax2.plot(recall, wujianbi)
            ax2.tick_params(axis='y')
        ax3 = fig.add_subplot(131)
        ax3.set_xlabel('confs')
        ax3.set_ylabel('F2_score')
        for f2s, confs in f2_score_list:
            ax3.plot(confs, f2s,)
        pic_name = os.path.join(os.path.dirname(self.pr_xml_path[0]), str(self.taget_label)+"_PRErrF2info.jpg")
        plt.savefig(pic_name)
        plt.clf()
        # plt.show()
        return pic_name

    def bad_case(self,conf_thershold,iou_thershold=0.5):#TODO:需要优化的代码 

        common_imgs = list(set([os.path.basename(i) for i in self.gt_xml_path]) & set([os.path.basename(i) for i in self.pr_xml_path]))

        bad_case_all = []
        for xml in common_imgs:
            gt_xml_dir = os.path.dirname(self.gt_xml_path[0])
            gt_xml_path = os.path.join(gt_xml_dir, xml)
            try:
                gt_objects = self.xmlRead(gt_xml_path)
            except Exception:
                print('----- read xml err ---->', os.path.join(gt_xml_dir, xml))

            pr_xml_dir = os.path.dirname(self.pr_xml_path[0])
            pr_xml_path = os.path.join(pr_xml_dir, xml)
            try:
                pr_objects = self.xmlRead(pr_xml_path)
            except Exception:
                print('----- read xml err ---->', os.path.join(pr_xml_dir, xml))
            iou_temp_all = []
            iou_temp_all2 = []
            for idx_pr,pr_obj in enumerate(pr_objects):
                pr_label, pr_prob, pr_box = pr_obj
                for idx_gt,gt_obj in enumerate(gt_objects):
                    gt_label, gt_prob, gt_box = gt_obj
                    iou_temp = self.calculate_iou(gt_box, pr_box)
                    iou_temp_all.append(iou_temp)
                    if  iou_temp>iou_thershold and gt_label == pr_label and pr_prob > conf_thershold:
                        pass #  excepted result
                    elif iou_temp>iou_thershold and gt_label != pr_label and pr_prob > conf_thershold:
                        bad_case_all.append([gt_label,pr_label,gt_box,pr_box,gt_xml_path,pr_xml_path]) # wujian
                    for idx_pr,pr_obj2 in enumerate(pr_objects):
                        pr_label2, pr_prob2, pr_box2 = pr_obj2
                        iou_temp2 = self.calculate_iou(pr_box2,gt_box)
                        iou_temp_all2.append(iou_temp2)
                try:
                    if max(iou_temp_all)<iou_thershold:
                        bad_case_all.append([gt_label,None,gt_box,None,gt_xml_path,None])
                    if max(iou_temp_all2)<iou_thershold:
                        bad_case_all.append([None,pr_label,None,pr_box,None,pr_xml_path])
                except:
                    continue

        bad_case_all_pr = [[i[3]] for i in bad_case_all]
        
        bad_case_all_gt = [i[2] for i in bad_case_all]
        for xml_path in tqdm(self.pr_xml_path,desc= "Bad Case Generating"):
            pr_path = os.path.splitext(xml_path)
            jpg_path = pr_path[0]+'.jpg'
            img = cv2.imread(jpg_path)
            res_pr_xml = self.xmlRead(pr_xml_path)
            for gt_path in self.gt_xml_path:
                gt_name = os.path.basename(gt_path)
                if gt_name == os.path.basename(xml_path):
                    res_gt_xml = self.xmlRead(gt_path)
                    # print(res_gt_xml)
                    for pr_smaple in res_pr_xml:
                        if pr_smaple[2] not in bad_case_all_pr: # Normal
                            try:
                                cv2.rectangle(img, (res_gt_xml[0][2][0], res_gt_xml[0][2][3]), (res_gt_xml[0][2][2], res_gt_xml[0][2][1]), color=(255, 255, 255),lineType=32 )#画矩形，参数2和3是矩形的左上角点和右下角点的坐标
                                cv2.putText(img, "normal_"+res_gt_xml[0][0], (res_gt_xml[0][2][0], res_gt_xml[0][2][1]-1), fontFace=cv2.CALIB_SAME_FOCAL_LENGTH, fontScale=1, color=(255, 255, 255),lineType=5)#在图片上附上文字，字体和字号和颜色
                            except:
                                continue
            for bad_sample in bad_case_all:
                try:#TODO: OPTIMIZE THIS CODE
                    if os.path.basename(bad_sample[4]) == os.path.basename(xml_path):
                        if bad_sample[0] == None and bad_sample[1] != None:
                            cv2.rectangle(img, (bad_sample[3][0], bad_sample[3][3]), (bad_sample[3][2], bad_sample[3][1]), color=(0, 0, 255),lineType=32)#画矩形，参数2和3是矩形的左上角点和右下角点的坐标
                            cv2.putText(img, "error_"+bad_sample[1], org= (bad_sample[3][0], bad_sample[3][1]-2), fontFace=cv2.CALIB_SAME_FOCAL_LENGTH,fontScale=1,color=(0, 0, 255),lineType=5)#在图片上附上文字，字体和字号和颜色
                        elif bad_sample[0] != None and bad_sample[1] == None:
                            cv2.rectangle(img, (bad_sample[2][0], bad_sample[2][3]), (bad_sample[2][2], bad_sample[2][1]), color=(0, 255, 255),lineType=32)#画矩形，参数2和3是矩形的左上角点和右下角点的坐标
                            cv2.putText(img, "loss_"+bad_sample[0], (bad_sample[2][0], bad_sample[2][1]-3), fontFace=cv2.CALIB_SAME_FOCAL_LENGTH,fontScale=1,color=(0, 255, 255),lineType=5)#在图片上附上文字，字体和字号和颜色
                        else:
                            cv2.rectangle(img, (bad_sample[3][0], bad_sample[3][3]), (bad_sample[3][2], bad_sample[3][1]), color=(255, 0, 255),lineType=32)#画矩形，参数2和3是矩形的左上角点和右下角点的坐标
                            cv2.putText(img, "misclass_"+bad_sample[1], (bad_sample[3][0], bad_sample[3][1]-4), fontFace=cv2.CALIB_SAME_FOCAL_LENGTH,fontScale=1, color=(255, 0, 255),lineType=5)#在图片上附上文字，字体和字号和颜色
                except:
                    if os.path.basename(bad_sample[5]) == os.path.basename(xml_path):
                        if bad_sample[0] == None and bad_sample[1] != None:
                            cv2.rectangle(img, (bad_sample[3][0], bad_sample[3][3]), (bad_sample[3][2], bad_sample[3][1]), color=(0, 0, 255),lineType=32)#画矩形，参数2和3是矩形的左上角点和右下角点的坐标
                            cv2.putText(img, "error_"+bad_sample[1], (bad_sample[3][0], bad_sample[3][1]-2), fontFace=cv2.CALIB_SAME_FOCAL_LENGTH,fontScale=1,color=(0, 0, 255),lineType=5)#在图片上附上文字，字体和字号和颜色
                        elif bad_sample[0] != None and bad_sample[1] == None:
                            cv2.rectangle(img, (bad_sample[2][0], bad_sample[2][3]), (bad_sample[2][2], bad_sample[2][1]), color=(0, 255, 255),lineType=32)#画矩形，参数2和3是矩形的左上角点和右下角点的坐标
                            cv2.putText(img, "loss_"+bad_sample[0], (bad_sample[2][0], bad_sample[2][1]-3), fontFace=cv2.CALIB_SAME_FOCAL_LENGTH,fontScale=1,color=(0, 255, 255),lineType=5)#在图片上附上文字，字体和字号和颜色
                        else:
                            cv2.rectangle(img, (bad_sample[3][0], bad_sample[3][3]), (bad_sample[3][2], bad_sample[3][1]), color=(255, 0, 255),lineType=32)#画矩形，参数2和3是矩形的左上角点和右下角点的坐标
                            cv2.putText(img, "misclass_"+bad_sample[1], (bad_sample[3][0], bad_sample[3][1]-4), fontFace=cv2.CALIB_SAME_FOCAL_LENGTH,fontScale=1,color=(255, 0, 255),lineType=5)#在图片上附上文字，字体和字号和颜色
            dirname_ = os.path.dirname(self.pr_xml_path[0])
            bad_case_folder = os.path.join(dirname_,'bad_case')
            if not os.path.exists(bad_case_folder):
                os.makedirs(bad_case_folder)
            save_name = os.path.join(bad_case_folder,os.path.basename(pr_path[0])+'.jpg')

            cv2.imwrite(save_name, img)
            bad_case_random = random.sample(bad_case_all,10)
            bad_case_path = []
            for bad_sample in bad_case_random:
                if bad_sample[0] == None and bad_sample[1] != None:
                    bad_case_path.append(os.path.join(bad_case_folder,os.path.basename(os.path.splitext(bad_sample[5])[0])+'.jpg'))
                elif bad_sample[0] != None and bad_sample[1] == None:
                    bad_case_path.append(os.path.join(bad_case_folder,os.path.basename(os.path.splitext(bad_sample[4])[0])+'.jpg'))
                else:
                    bad_case_path.append(os.path.join(bad_case_folder,os.path.basename(os.path.splitext(bad_sample[5])[0])+'.jpg'))

        return bad_case_path




    
    def F2_score(self, recall, precison):
        f2 = 5 * precison * recall / (1 * recall + 4 * precison)
        return round(f2, 6)


    def F1_score(self, recall, precison):
        f1 = 2 * precison * recall / (recall + precison)
        return round(f1, 6)

    def main(self):
        
        print('----------------------------- {} ----------------------------------'.format(self.taget_label))
        gt_K_num = self.objects_count_xml(self.gt_xml_path, 1, gt=True)
        print('图片张数：{}，gt_num:{}'.format(len(self.gt_xml_path), gt_K_num))

        pare_list = []
        pare_listL = []
        f2_score_list = []


        step = 0.1 * 1
        recalls = []
        precisons = []
        f2_scores = []
        confs = []
        wujianbis = []

        for i in range(0, int(1 / step)):
            conf_thershold = round(i * step, 3)
            recall, precision = self.caculate_PR(conf_thershold)

            wujianbi = (1 / (precision - 0.0000001) - 1) * recall
            wujianbis.append(wujianbi)

            recall = recall if recall > 0 else recalls[-1]
            recalls.append(recall)
            precision = precision if precision > 0 else precisons[-1]
            precisons.append(precision)

            f2_scores.append(self.F2_score(recall, precision))

            print('\trecall = {}, precision={} ,wujianbi={} ,F2score={}| {}'.format(recall, precision, wujianbi,
                                                                                    self.F2_score(recall, precision),
                                                                                    conf_thershold))

            confs.append(conf_thershold)
        pare_list.append(((precisons), (recalls)))
        pare_listL.append(((precisons), (recalls), (wujianbis)))
        f2_score_list.append((f2_scores, confs))

        print("\t##  draw PR curve ##")
        result_path = self.plot_prs_PRE_F2(pare_listL, f2_score_list)
        return result_path

if __name__ == "__main__":

    xml = XmlUtils()
    xml.main()





    