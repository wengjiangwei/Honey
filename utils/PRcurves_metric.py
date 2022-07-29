import os
import xml.etree.ElementTree as ET
import shutil
import matplotlib
# matplotlib.use("Agg")
import matplotlib.pyplot as plt


def xmlRead(xml_path, taget_label):
    voc_labels = []
    tree = ET.parse(xml_path)
    root = tree.getroot()

    for obj in root.iter('object'):
        label = obj.find('name').text
        if label != taget_label:
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


def objects_count_xml(xml_list, xml_dir, taget_label, conf_thershold, gt=False):
    tot_objects = []

    for xml in xml_list:
        xml_path = os.path.join(xml_dir, xml)
        try:
            objects = xmlRead(xml_path, taget_label)
        except Exception:
            print('----- read xml err ---->', xml_path)
        if len(objects) != 0:
            if not gt:
                objects = [obj for obj in objects if obj[1] > conf_thershold]
            tot_objects.extend(objects)

    results = len([obj for obj in tot_objects if obj[0] == taget_label])
    return results


def calculate_iou(gt, pr):
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


def caculate_PR(pr_xml_dir, taget_label, conf_thershold):
    pr_xml_list = [xml for xml in os.listdir(pr_xml_dir) if xml.endswith(".xml")]
    common_imgs = list(set(gt_xml_list) & set(pr_xml_list))

    correct_inference_list = []  ## 正确目标 ##
    extra_inference_list = []  ## 多检目标 ##

    correct_num = objects_count_xml(gt_xml_list, gt_xml_dir, taget_label, conf_thershold, gt=True)

    total_num = objects_count_xml(pr_xml_list, pr_xml_dir, taget_label, conf_thershold, gt=False)

    for xml in common_imgs:
        gt_xml_path = os.path.join(gt_xml_dir, xml)
        try:
            gt_objects = xmlRead(gt_xml_path, taget_label)
        except Exception:
            print('----- read xml err ---->', os.path.join(gt_xml_dir, xml))

        pr_xml_path = os.path.join(pr_xml_dir, xml)
        try:
            pr_objects = xmlRead(pr_xml_path, taget_label)
        except Exception:
            print('----- read xml err ---->', os.path.join(pr_xml_dir, xml))

        for pr_obj in pr_objects:
            pr_label, pr_prob, pr_box = pr_obj

            for gt_obj in gt_objects:
                gt_label, gt_prob, gt_box = gt_obj

                ## 正确 和 多检 ##
                if pr_label == gt_label and pr_prob > conf_thershold:
                    iou = calculate_iou(gt_box, pr_box)
                    if iou > iou_thershold:
                        correct_inference_list.append((xml, pr_box))

                    else:
                        extra_inference_list.append((xml, pr_box))

    correct_inference_num = len(correct_inference_list)

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


def plot_prs_PRE_F2(pare_listL, f2_score_list, taget_label, area=''):
    fig = plt.figure()

    ax1 = fig.add_subplot(132)
    ax1.set_title(str(taget_label) + '|iou_thershold=' + str(iou_thershold))
    ax1.set_xlabel('Recall')
    ax1.set_ylabel('Precision')
    # plt.xlim(0.7,1.0)
    # plt.ylim(0.5,1.0)
    for (model_id, precision, recall, wujianbi) in pare_listL:
        ax1.plot(recall, precision, color=color_dict[model_id + 1][0], marker=color_dict[model_id + 1][1],
                 label=str(model_i_dict[model_id + 1]))
        ax1.legend(loc=0, ncol=2)

    ax2 = fig.add_subplot(133)
    ax2.set_xlabel('Recall')
    ax2.set_ylabel('ErrRate')

    for (model_id, precision, recall, wujianbi) in pare_listL:
        ax2.plot(recall, wujianbi, color=color_dict[model_id + 1][0], marker=color_dict[model_id + 1][1])
        ax2.tick_params(axis='y')

    ax3 = fig.add_subplot(131)
    ax3.set_xlabel('confs')
    ax3.set_ylabel('F2_score')
    for (model_id, f2s, confs) in f2_score_list:
        plt.plot(confs, f2s, color=color_dict[model_id + 1][0], marker=color_dict[model_id + 1][1],
                 label=str(model_i_dict[model_id + 1]))
        # plt.legend(loc=0, ncol=2)

    pic_name = os.path.join(rs_picDir, (area + "_PRErrF2info.jpg"))
    # plt.savefig(pic_name)

    plt.show()


def F2_score(recall, precison):
    f2 = 5 * precison * recall / (1 * recall + 4 * precison)
    return round(f2, 6)


def F1_score(recall, precison):
    f1 = 2 * precison * recall / (recall + precison)
    return round(f1, 6)


if __name__ == "__main__":

    gt_xml_dir = r"E:\Data\杆塔_破损_测试数据"
    version = 'kkxAllin_s3000'
    area = 'std3600'
    rs_picDir = os.path.join("rs_rust_pic", version)
    os.makedirs(rs_picDir, exist_ok=True)

    gt_xml_list = [xml for xml in os.listdir(gt_xml_dir) if xml.endswith(".xml")]

    iou_thershold = 0.5

    taget_labels = ['gttd_ps']  # 'kkxObj_miss','kkxObj_illegal','dpObj_miss'

    ### 预测结果xml路径list ###
    pr_xml_dir1 = os.path.join(r'C:\Users\txkj\Desktop\merge')
    # pr_xml_dir2 = os.path.join(r'F:\销钉缺失\merge_v1.0')
    # pr_xml_dir3 = os.path.join(r'K:\【标准】测试集\开口销缺失\【全域3K】\测试结果\v1460_conf0.3\merge - kkxObjrename')
    # pr_xml_dir4 = os.path.join(r'K:\【标准】测试集\开口销缺失\【全域3K】\测试结果\v1500_conf0.3-修正2\merge')
    # pr_xml_dir5 = os.path.join(r'K:\【标准】测试集\开口销缺失\【全域3K】\测试结果\kkxAllin_s3000-newStep2\merge')
    # pr_xml_dir6 = os.path.join(r'K:\【标准】测试集\开口销缺失\【全域3K】\测试结果\v1500_conf0.3-修正\merge')

    pr_xmls = []
    pr_xmls.append(pr_xml_dir1)
    # pr_xmls.append(pr_xml_dir2)
    # pr_xmls.append(pr_xml_dir3)
    # pr_xmls.append(pr_xml_dir4)
    # pr_xmls.append(pr_xml_dir5)
    # pr_xmls.append(pr_xml_dir6)

    model_i_dict = {1: 'v1.2'}
    color_dict = {1: ('red', 'o')}
    # model_i_dict = {1: 'nc_v1190', 2: 'v1470', 3: 'v1460', 4: 'v1500fix', 5: 's3000-newS2',6: 'v1500-fix'}
    # color_dict = {1: ('blue', 's'), 2: ('lightcoral', 'o'), 3: ('deepskyblue', 'v'), 4: ('orange', 'D'), 5: ('gold', "o"), 6: ('cyan', "o")}# orange  #deepskyblue   #cyan青色  #gold金色  #lightcoral红色  #green绿色

    for taget_label in taget_labels:
        print('----------------------------- {} ----------------------------------'.format(taget_label))
        gt_K_num = objects_count_xml(gt_xml_list, gt_xml_dir, taget_label, 1.0, gt=True)
        print('图片张数：{}，gt_num:{}'.format(len(gt_xml_list), gt_K_num))

        pare_list = []
        pare_listL = []
        f2_score_list = []

        step = 0.1 * 1
        for model_i, pr_xml_dir in enumerate(pr_xmls):
            print('*** {} ***'.format(pr_xml_dir))
            recalls = []
            precisons = []
            f2_scores = []
            confs = []
            wujianbis = []

            for i in range(0, int(1 / step)):
                conf_thershold = round(i * step, 3)
                recall, precision = caculate_PR(pr_xml_dir, taget_label, conf_thershold)

                wujianbi = (1 / (precision - 0.001) - 1) * recall
                wujianbis.append(wujianbi)

                recall = recall if recall > 0 else recalls[-1]
                recalls.append(recall)
                precision = precision if precision > 0 else precisons[-1]
                precisons.append(precision)

                f2_scores.append(F2_score(recall, precision))

                print('\trecall = {}, precision={} ,wujianbi={} ,F2score={}| {}'.format(recall, precision, wujianbi,
                                                                                        F2_score(recall, precision),
                                                                                        conf_thershold))

                confs.append(conf_thershold)
            pare_list.append((model_i, (precisons), (recalls)))
            pare_listL.append((model_i, (precisons), (recalls), (wujianbis)))
            f2_score_list.append((model_i, f2_scores, confs))

        print("\t##  draw PR curve ##")
        plot_prs_PRE_F2(pare_listL, f2_score_list, taget_label, area)
