#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# version: v1.0
# author : 袁润和
# Project : ythWhleProject
# File : account.py
# Software: PyCharm
# time: 2023/5/7 14:05
"""

from django.shortcuts import HttpResponse
from projectManagement.utils.yzm import check_code
from io import BytesIO  # 将数据写到内存中去
from projectManagement.utils import redisBK


def image_code(request):
    img, code = check_code()  # 调用
    stream = BytesIO()  # 创建一个内存地址
    img.save(stream, 'png')  # 将图片保存到内存中去

    # 获取随机字符串
    key = redisBK.get_code_key(10)
    # 数据保存到redis
    redisBK.set_redis_key_code(key, code)

    # 将数据写到session中，前端验证通过这个获取
    request.session['image_code'] = key
    # 获取数据
    # print(redisBK.get_dict_value(key))

    return HttpResponse(stream.getvalue())
