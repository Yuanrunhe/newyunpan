#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# version: v1.0
# author : 袁润和
# Project : ythWhleProject
# File : ModelForm.py
# Software: PyCharm
# time: 2023/4/15 14:00
"""

from django import forms
from django.forms import ModelForm, ValidationError
from newyunpan.models import FolderBook


# 创建文件夹
class CreateFolder(ModelForm):
    class Meta:
        model = FolderBook
        fields = ["folder_name"]

        widgets = {
            "folder_name": forms.TextInput(attrs={"class": "create_folder_name form-control",
                                                  "id": "create_folder_name",
                                                  "name": "create_folder_name",
                                                  "placeholder": "新建文件夹"})
        }
