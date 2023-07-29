#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# version: v1.0
# author : 袁润和
# Project : ythWhleProject
# File : redis-cz.py
# Software: PyCharm
# time: 2023/5/8 22:15
"""

# from django.core.cache import cache

from django_redis import get_redis_connection
import random
import string

login_code_conn = get_redis_connection("login_code")  # 根据名称连接


def get_dict_value(key):
    # 如果key存在，则返回对应的值；否则返回None
    return login_code_conn.get(key)


# 随机生成30位字符串
def get_code_key(length):
    # 随机选择字母和数字
    letters_and_digits = string.ascii_letters + string.digits
    k1 = ''.join(random.choice(letters_and_digits) for i in range(length))
    letters_and_digits = string.ascii_letters + string.digits
    k2 = ''.join(random.choice(letters_and_digits) for i in range(length))
    letters_and_digits = string.ascii_letters + string.digits
    k3 = ''.join(random.choice(letters_and_digits) for i in range(length))

    key = k1 + k2 + k3

    # 生成随机字符串
    return key


# 保存验证码
def set_redis_key_code(key, code):
    login_code_conn.set(key, code, 60)
