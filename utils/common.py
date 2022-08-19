#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   common.py
@Time    :   2022/08/12 11:34:47
@Author  :   Weng Jiangwei 
@Github :    https://github.com/wengjiangwei
@Desc    :   None
'''


import os
import re
def report_max_idx(project_path:str, name:str)->str:
    """Find the latest version of the project save path
    (According to the max index of the project)

    Parameters
    ----------
    project_path : str
        the  project save path
    name : str
        project_version

    Returns
    -------
    str
        the latest version of the project save path
    """
    project_all = []
    project_list = os.listdir(project_path)
    for filename in project_list:
        if name in filename:
            try:
                project_idx = re.findall("\d+", filename)
                project_all.append(int(project_idx[0]))
            except Exception:
                continue
    try:
        return os.path.join(project_path, f"{name}{max(project_all)}")
    except :
        return os.path.join(project_path, f"{name}")
