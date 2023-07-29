#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# version: v1.0
# author : 袁润和
# Project : ythWhleProject
# File : uploaded_folder.py
# Software: PyCharm
# time: 2023/4/26 23:59
"""

import os
import shutil


def handle_upload_folder(upload_folder):
    # 获取上传文件夹的绝对路径
    upload_path = os.path.abspath(upload_folder)

    # 遍历上传文件夹中的所有文件和子文件夹
    for root, dirs, files in os.walk(upload_path):
        # 计算当前文件/文件夹的相对路径（相对于上传文件夹）
        relative_path = os.path.relpath(root, upload_path)

        # 根据相对路径获取当前文件/文件夹所处的层级
        level = len(relative_path.split(os.path.sep)) - 1

        # 输出当前文件/文件夹的名称和所处的层级
        print('-' * level + os.path.basename(root) + '/')

        # 处理当前文件夹中的文件
        for file in files:
            # 输出当前文件的名称和所处的层级
            print('-' * (level + 1) + file)

        # 处理当前文件夹中的子文件夹
        for sub_dir in dirs:
            # 递归处理子文件夹
            handle_upload_folder(os.path.join(root, sub_dir))


# 调用函数，处理上传的文件夹
handle_upload_folder('path/to/upload/folder')
