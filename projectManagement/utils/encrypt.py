#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# version: v1.0
# author : 袁润和
# Project : Django项目
# File : encrypt.py
# Software: PyCharm
# time: 2023/3/18 23:27
# 制定密码的加密方式
"""
from django.conf import settings  # 导入配置文件
import hashlib


def md5(data_string):
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))  # 加盐，用Django配置文件自带的字符串
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()
