#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# version: v1.0
# author : 袁润和
# Project : ythWhleProject
# File : AutoLogin.py
# Software: PyCharm
# time: 2023/5/8 23:28
"""

from django.utils.deprecation import MiddlewareMixin
from projectManagement.models import user_info
from django.shortcuts import redirect, render
from newyunpan.models import NewUserInfo


# class AutoLogin(MiddlewareMixin):
#     def process_request(self, request):
#         # 1.排除不需要登录验证的链接
#         pc_url = ["/login/", "/register/", "/image/code/"]
#         if request.path_info in pc_url:
#             return
#         info_dict = request.session.get("info")
#         # 有cookie数据
#         if info_dict:
#             # 验证账号密码是否存在或者密码是否正确
#             admin_log = user_info.objects.filter(**info_dict).first()
#             # 正确情况，继续走下去
#             if admin_log:
#                 return
#             # 不正确情况进去登录界面
#             request.session.clear()
#             return redirect("/login/")
#         return redirect("/login/")


# 新model
class AutoLogin(MiddlewareMixin):
    def process_request(self, request):
        # 1.排除不需要登录验证的链接
        pc_url = ["/login/", "/register/", "/image/code/"]
        if request.path_info in pc_url:
            return
        info_dict = request.session.get("info")
        # 有cookie数据
        if info_dict:
            # 验证账号密码是否存在或者密码是否正确
            admin_log = NewUserInfo.objects.filter(**info_dict).first()
            # 正确情况，继续走下去
            if admin_log:
                return
            # 不正确情况进去登录界面
            request.session.clear()
            return redirect("/login/")
        return redirect("/login/")
