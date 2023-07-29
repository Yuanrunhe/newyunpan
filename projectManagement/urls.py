#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# version: v1.0
# author : 袁润和
# Project : ythWhleProject
# File : urls.py.py
# Software: PyCharm
# time: 2023/5/13 16:01
"""
from django.urls import path
from .views import yunpan

urlpatterns = [
    # 云盘 yunpan/
    path('', yunpan.yunpan),
    path('load_file/', yunpan.load_file),
    path('del_file/', yunpan.del_file),
    path('add_folder/', yunpan.add_folder, name="add_folder"),
    path('api/getfirst/', yunpan.get_first_yunpan, name="getfirst"),
    path('api/getsecond/', yunpan.get_second_yunpan, name="getsecond"),
    path('api/getthird/', yunpan.get_third_yunpan, name="getthird"),
    path('api/creatfolder/', yunpan.create_folder, name="creatfolder"),
]
