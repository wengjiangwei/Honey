#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   ReportUtils.py
@Time    :   2022/08/11 09:48:04
@Author  :   Weng Jiangwei 
@Github :    https://github.com/wengjiangwei
@Desc    :   Export the results PDF file
'''


from importlib.resources import Package
import itertools
from abc import  ABCMeta, abstractmethod
import os
from pylatex import Document, Section, Subsection, Command, LongTable,Figure,Package
from pylatex.utils import italic, NoEscape
import yaml
import csv

class Report_base(metaclass=ABCMeta):
    """Report_base contains abstractmethod read and write methods

    Parameters
    ----------
    metaclass : _type_, optional
        _description_, by default ABCMeta
    """    
    @abstractmethod
    def read(self):
        '''read the generated files
        '''
        pass

    @abstractmethod
    def write(self):
        '''write the results to latex file
        '''
        pass

class TrainReport_yolov5(Report_base):
    """Function is suitable for YOLOv5 to format the latex and PDF files

    Parameters
    ----------
    Report_base : _type_
        _description_
    """    
    def __init__(self,root_path:str,PDF_path:str):
        """
        Parameters
        ----------
        root_path : str
            the path of save folder
        PDF_path  : str
            PDF save path
        """
        super(TrainReport_yolov5, self).__init__()
        self.root_path = root_path
        self.PDF_path = PDF_path
        if not os.path.exists(self.PDF_path):
            os.makedirs(self.PDF_path)
        self.read()

    def read(self):#TODO: EXPORT the file type ~

        self.imgs_path = []
        self.imgs_name = []
        self.csvs_path = []
        self.csvs_name = []
        self.yaml_path = []
        self.yaml_name = []
        file_list = os.listdir(self.root_path)

        for file_name in file_list:
            file_path = os.path.join(self.root_path, file_name)
            (filepath,tempfilename) = os.path.split(file_path)
            (filename,extension) = os.path.splitext(tempfilename)
            if not os.path.isfile(file_path):
                continue
            if extension in ['.jpg','.JPG','.png']:
                self.imgs_path.append(file_path)
                self.imgs_name.append(filename)
            if extension in ['.csv']:
                self.csvs_path.append(file_path)
                self.csvs_name.append(filename)
            if extension in ['.yaml']:
                self.yaml_path.append(file_path)
                self.yaml_name.append(filename)

        print("Loading  ... ")
        print(f"{self.imgs_name}\n")
        print(f"{self.csvs_name}\n")
        print(f"{self.yaml_name}\n")
            

    def write(self, project_infor:list):
        """write the read_informations to generate the latex file
        Note that: project_infor is normalized==>[[project_name, project_developer]]

        Parameters
        ----------
        project_infor : list
            [project_name, project_developer]
        """        
        
        geometry_options = {
        "margin": "2.54cm",
        "includeheadfoot": True
                                }
        doc = Document('report',geometry_options=geometry_options)
        doc.packages.append(Package('float'))
        doc.preamble.append(Command('title', f'Training Report {project_infor[0]}'))
        doc.preamble.append(Command('author', f'{project_infor[1]}'))
        doc.preamble.append(Command('date', NoEscape(r'\today')))

        doc.append(NoEscape('\maketitle'))
        self._fill_document(doc)
        doc.generate_pdf(os.path.join(self.PDF_path,f'report {project_infor[0]}'), clean_tex=False)
        tex = doc.dumps()
        return os.path.join(self.PDF_path,f'report {project_infor[0]}.pdf') # PDF Document


    def _fill_document(self, doc):
        """kernel function to write the tex statements.
        1. yaml file
        2. csv file
        3.image

        Parameters
        ----------
        doc : pylatex module
            doc = Document('report',geometry_options=geometry_options)
        """
        section_name = ['Setting Information', 'Training Information', 'Training Results']
        subsection_name = [self.yaml_name, self.csvs_name, self.imgs_name]
        for idx, file in enumerate([self.yaml_path, self.csvs_path, self.imgs_path]):
            # idx denotes the file type
            with doc.create(Section(section_name[idx])):
                if idx == 0:
                    doc.append('Setting Information, include project settings and yolo model settings.\n')
                    doc.append(italic("Note that: key parameter is image size and project save path."))
                    except_index = ['opt','hyp']  # change the index of the list with except index

                elif idx == 1:
                    doc.append('Training Information contains the loss values and performance index.')
                    except_index = ['results']

                elif idx == 2:
                    doc.append('Training Results is formed with input batch images, label distribution, performance curve and confusion matrix.')
                    except_index = ['train_batch0','train_batch1','train_batch2','val_batch0_labels','val_batch0_pred',\
                                'val_batch1_labels','val_batch1_pred','F1_curve', 'PR_curve', 'R_curve', 'P_curve', \
                                'results', 'labels','labels_correlogram', 'confusion_matrix']

                for idx_except in  except_index:
                    idx_sub = subsection_name[idx].index(idx_except)
                    with doc.create(Subsection(subsection_name[idx][idx_sub])):
                        if idx == 0:
                            with open(file[idx_sub], 'r', encoding='utf-8') as f:
                                data = yaml.load(f.read(), Loader=yaml.SafeLoader)
                                with doc.create(LongTable("c c")) as data_table:
                                    data_table.add_hline()
                                    data_table.add_row(["Parameters", "Values"])
                                    data_table.add_hline()
                                    data_table.end_table_header()
                                    data_table.add_hline()
                                    # data_table.add_row((MultiColumn(2, align='r', data='Continued on Next Page'),))

                                    data_table.add_hline()
                                    data_table.end_table_footer()
                                    data_table.add_hline()
                                    # data_table.add_row((MultiColumn(2, align='r', data='Continued on Next Page'),))

                                    data_table.add_hline()
                                    data_table.end_table_last_footer()

                                    for key, value in data.items():
                                        data_table.add_row([key,value])
                        elif idx == 1:

                            csv_reader = csv.reader(open(file[idx_sub]),)
                            csv_reader.__next__()
                            with doc.create(LongTable("c c c c c c c")) as data_table:
                                data_table.add_hline()
                                data_table.add_row(['epoch',' train/box_loss','train/obj_loss','train/cls_loss','precision',\
                                        'recall','mAP_0.5',])
                                data_table.add_hline()
                                data_table.end_table_header()
                                data_table.add_hline()
                                # data_table.add_row((MultiColumn(7, align='r', data='Continued on Next Page'),))

                                data_table.add_hline()
                                data_table.end_table_footer()
                                data_table.add_hline()
                                # data_table.add_row((MultiColumn(7, align='r', data='Continued on Next Page'),))

                                data_table.add_hline()
                                data_table.end_table_last_footer()
                                for line in csv_reader:
                                    data_table.add_row(line[:7])
                            csv_reader = csv.reader(open(file[idx_sub]),)
                            csv_reader.__next__()
                            with doc.create(LongTable("c c c c c c c c")) as data_table:
                                    data_table.add_hline()
                                    data_table.add_row(['epoch','mAP_0.5:0.95','val/box_loss','val/obj_loss',\
                                            'val/cls_loss','x/lr0','x/lr1','x/lr2'])
                                    data_table.add_hline()
                                    data_table.end_table_header()
                                    data_table.add_hline()
                                    # data_table.add_row((MultiColumn(8, align='r', data='Continued on Next Page'),))

                                    data_table.add_hline()
                                    data_table.end_table_footer()
                                    data_table.add_hline()
                                    # data_table.add_row((MultiColumn(8, align='r', data='Continued on Next Page'),))

                                    data_table.add_hline()
                                    data_table.end_table_last_footer()
                                    for line in csv_reader:
                                        data_temp = line[7:]
                                        data_temp.insert(0,line[0])
                                        data_table.add_row(data_temp)
                        elif idx == 2:
                            with doc.create(Figure(position='H')) as plot:
                                plot.add_image(file[idx_sub], width=NoEscape(r'0.5\linewidth'))
                                # plot.add_caption('I am a caption.')

                    # TODO: BAD CASE analyse

                            
                            


if __name__ == '__main__':
    SAVE_PROJECT_PATH = r"/home/wjw/Work/Runs/v5-ft/ft8"
    SVAE_PDF_PATH = r"/home/wjw/Work/YOLOV5_PDF"
    PROJECT_INFOR = ["ft_v1","WENGJIANGWEI"]
    res = TrainReport_yolov5(SAVE_PROJECT_PATH,SVAE_PDF_PATH)
    res.write(PROJECT_INFOR)
    # res.read()

