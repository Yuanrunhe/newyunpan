#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# version: v1.0
# author : 袁润和
# Project : ythWhleProject
# File : ypUrl.py
# Software: PyCharm
# time: 2023/7/1 22:19
"""

from django.urls import path
from .views import newYP

urlpatterns = [
    # 云盘 yunpan/
    path('', newYP.newyp),
    path('upfile/', newYP.up_file_view),
    path('crFolder/', newYP.create_Folder),
    path('getPageFile/', newYP.getPageFile),
    path('rtupData/', newYP.getrtupData),
    path('fileDown/', newYP.fileDown),
    path('delete/', newYP.deleteFile),
]
