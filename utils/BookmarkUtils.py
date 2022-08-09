#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   BookmarkUtils.py
@Time    :   2022/08/09 16:16:02
@Author  :   Weng Jiangwei 
@Github :    https://github.com/wengjiangwei
@Desc    :   None
'''

import os
import chardet # check file encoding type
import re
from tqdm import tqdm
import shutil 

class BookmarkUtils():
    """
    1. "Honeyview" software + Bookmark tools ==> Bookmark files
    2. select bookmark_path (allow multiple bookmark files with list format) and sava_path
    3. coping mode or moving mode (warning !!! )
    Note that : Please delete the history bookmark results manually in Honeyview software !
    """    
    def __init__(self, bookmark_path:list,save_path:str):
        self.bookmark_path = bookmark_path
        self.save_path = save_path
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        self._check_charset()
        self._desc_bookmark()

    def copy_imgs(self):
        """copy images 
        """        
        for img_path in tqdm(self.imgs_path,desc='Image croping'): 
            img_name = os.path.basename(img_path)
            shutil.copyfile(img_path,os.path.join(self.save_path,img_name))

    
    def move_imgs(self):
        """move images
        """        
        check_result = input("Please check the bookmark file carefully. check: 1 or break: 0 :::")
        if  check_result== '1' or check_result== "check":
            for img_path in tqdm(self.imgs_path,desc='Images moving'): 
                img_name = os.path.basename(img_path)
                shutil.move(img_path,os.path.join(self.save_path,img_name))
        elif check_result== '0' or check_result== "break":
            print("Break the code")
        else:
            print("Wrong check result")


    
    def _desc_bookmark(self):
        """read the bookmarks files and convert the path with re_method.
        """        
        self.imgs_path =[]
        for i, path_i in  enumerate(self.bookmark_path):
            with open(path_i,encoding=self.type_encoding[i]) as f:
                img_sets = f.readlines()
                for img_fixed in img_sets:
                    if re.search(r".*=.*",img_fixed):
                        _img = re.findall(r'= (.+?)\n',img_fixed)
                        self.imgs_path.append(_img[0])
        print(f'the size of Image sets is {len(self.imgs_path)}')
        print(f'root image path is {self.bookmark_path}')
        print(f'save image path is {self.save_path}')


    def _check_charset(self):
        """bookmark files encoding check.
        """        
        self.type_encoding = []
        for path_i in self.bookmark_path:
            with open(path_i,'rb') as f:
                data = f.read(10)
                charset = chardet.detect(data)['encoding']
            self.type_encoding.append(charset)

    

if __name__ == '__main__':

    bookmark_path = [...]
    save_path = ...
    bookmarks = BookmarkUtils(bookmark_path,save_path)
    # bookmarks.copy_imgs()
    # bookmarks.move_imgs()