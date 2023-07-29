#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# version: v1.0
# author : 袁润和
# Project : ythWhleProject
# File : form.py
# Software: PyCharm
# time: 2023/7/12 22:40
"""

from django import forms


# 上传文件
class UploadFolderForm(forms.Form):
    directory = forms.FileField(label="请点击按钮上传文件",
                                widget=forms.ClearableFileInput(
                                    attrs={
                                        'class': "up-file-gn-nt form-group",
                                        # 'multiple': True,
                                        # 'webkitdirectory': True,
                                        # 'directory': True
                                    }
                                ))
