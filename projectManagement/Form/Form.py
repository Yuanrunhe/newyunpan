#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# version: v1.0
# author : 袁润和
# Project : ythWhleProject
# File : Form.py
# Software: PyCharm
# time: 2023/4/26 22:14
"""

from django import forms

# 上传文件
class UploadFolderForm(forms.Form):
    directory = forms.FileField(label="文件名",
                                widget=forms.ClearableFileInput(
                                    attrs={
                                        'class': "form-group",
                                        # 'multiple': True,
                                        'webkitdirectory': True,
                                        'directory': True}
                                ))
