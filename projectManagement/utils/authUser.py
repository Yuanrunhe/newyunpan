#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# version: v1.0
# author : 袁润和
# Project : ythWhleProject
# File : authUser.py
# Software: PyCharm
# time: 2023/5/11 21:23
"""
from django.shortcuts import redirect
from projectManagement.models import user_info
from newyunpan.models import NewUserInfo


class User_auth:
    def __init__(self, request):
        self.request = request
        # self.person = self.request.session.get("info")["name"]
        # self.user_id = self.request.session.get("info")["user_nub"]
        self.person = self.request.session.get("info")["user_name"]
        self.user_id = self.request.session.get("info")["user_id"]

        self.user_object = NewUserInfo.objects

    # 用户验证
    def verify(self):
        user_verify = self.user_object.filter(user_id=self.user_id, user_name=self.person).first()
        if not user_verify:
            print("用户session问题")
            return redirect("/login/")

    # 获取session用户
    def get_person(self):
        if not self.person:
            return redirect("/login/")
        return self.person

    # 获取session用户ID
    def get_user_id(self):
        if not self.user_id:
            return redirect("/login/")
        return self.user_id

    # 获取model
    def get_model(self):
        user_object = self.user_object.filter(user_id=self.user_id, user_name=self.person).first()
        if not user_object:
            print("用户session问题")
            return redirect("/login/")
        return user_object

    # 获取关联数据
    def fkID(self):
        user_object = self.user_object.get(user_id=self.user_id)
        if not user_object:
            print("查无该用户")
            return redirect("/login/")
        return user_object
