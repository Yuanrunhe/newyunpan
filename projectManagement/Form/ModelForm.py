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
from projectManagement.models import project_info, note_info, user_info
from projectManagement.utils.encrypt import md5
from newyunpan.models import NewUserInfo


class projectInfoModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # 先判断是否存在，存在就直接添加，没有在创建
            if "file" in name:
                field.widget.attrs = {"class": "form-group", "placeholder": field.label}
            else:
                if field.widget.attrs:
                    field.widget.attrs = {"class": "form-control", "placeholder": field.label}
                else:
                    field.widget.attrs = {"class": "form-control", "placeholder": field.label}


class add_projrct_info(projectInfoModelForm):
    class Meta:
        model = project_info
        fields = ["project_name", "project_file", "remarks"]

    def clean_project_file(self):
        file = self.cleaned_data.get("project_file")
        if not file:
            raise ValidationError("请上传文件")
        elif file.size > 600 * 1024 * 1024:
            raise ValidationError("文件太大，请上传小于20M的文件")
        return file


# 编辑功能未完善
class edit_project_info(projectInfoModelForm):
    class Meta:
        model = project_info
        fields = ["project_name", "project_file", "remarks"]

    def clean_project_file(self):
        file = self.cleaned_data.get("project_file")
        if not file:
            raise ValidationError("请上传文件")
        elif file.size > 20 * 1024 * 1024:
            raise ValidationError("文件太大，请上传小于20M的文件")
        return file


# 笔记添加
class add_note_info(projectInfoModelForm):
    class Meta:
        model = note_info
        fields = ["note_name", "note_file", "remarks"]

    def clean_note_file(self):
        file = self.cleaned_data.get("note_file")
        if not file:
            raise ValidationError("请上传文件")
        elif file.size > 20 * 1024 * 1024:
            raise ValidationError("文件太大，请上传小于20M的文件")
        return file


# 旧的用户登录model
# class login_modelform(ModelForm):
#     class Meta:
#         model = user_info
#         fields = ['number', 'password']
#
#         widgets = {
#             "number": forms.TextInput(attrs={"id": "username",
#                                              "name": "username",
#                                              "placeholder": "请输入手机号"}),
#             "password": forms.PasswordInput(attrs={"id": "password",
#                                                "name": "password",
#                                                "placeholder": "请输入密码"})
#         }
#
#     def clean_password(self):
#         pwd = self.cleaned_data["password"]
#         return md5(pwd)

class login_modelform(ModelForm):
    class Meta:
        model = NewUserInfo
        fields = ['user_num', 'user_passwd']

        widgets = {
            "user_num": forms.TextInput(attrs={"id": "user_num",
                                               "name": "user_num",
                                               "placeholder": "请输入手机号"}),
            "user_passwd": forms.PasswordInput(attrs={"id": "user_passwd",
                                                      "name": "user_passwd",
                                                      "placeholder": "请输入密码"})
        }

    def clean_user_passwd(self):
        pwd = self.cleaned_data["user_passwd"]
        return md5(pwd)


# 就model验证
# class register_modelform(ModelForm):
#     confirm_password = forms.CharField(
#         label="确认密码",
#         widget=forms.PasswordInput(attrs={"class": "input_t",
#                                           "id": "confirm_password",
#                                           "name": "confirm_password",
#                                           "placeholder": "确认密码"})
#     )
#
#     class Meta:
#         model = user_info
#         fields = ["number", "name", "password", "confirm_password"]
#
#         widgets = {
#             "number": forms.TextInput(attrs={"class": "input_t",
#                                              "id": "username",
#                                              "name": "username",
#                                              "placeholder": "请输入手机号"}),
#             "password": forms.PasswordInput(attrs={"class": "input_t",
#                                                    "id": "password",
#                                                    "name": "password",
#                                                    "placeholder": "请输入密码",
#                                                    "render_value": True}),
#             "name": forms.TextInput(attrs={"class": "input_t",
#                                            "id": "name",
#                                            "name": "name",
#                                            "placeholder": "请输入姓名"})
#         }
#
#     # 验证号码是否已存在
#     def clean_number(self):
#         number = self.cleaned_data["number"]
#         number_models = user_info.objects.filter(number=number).exists()
#         if number_models:
#             raise ValidationError("注册号码已存在，请直接登录")
#         else:
#             return number
#
#     # 密码进行加密
#     def clean_password(self):
#         password = md5(self.cleaned_data["password"])
#         return password
#
#     # 两次密码进行验证
#     def clean_confirm_password(self):
#         text_password = self.cleaned_data["password"]
#         text_confirm_password = md5(self.cleaned_data["confirm_password"])
#         if text_password != text_confirm_password:
#             raise ValidationError("输入两次密码不匹配")
#         return text_confirm_password


class register_modelform(ModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(attrs={"class": "input_t",
                                          "id": "confirm_password",
                                          "name": "confirm_password",
                                          "placeholder": "确认密码"})
    )

    class Meta:
        model = NewUserInfo
        fields = ["user_num", "user_name", "user_passwd", "confirm_password"]

        widgets = {
            "user_num": forms.TextInput(attrs={"class": "input_t",
                                               "id": "user_num",
                                               "name": "user_num",
                                               "placeholder": "请输入手机号"}),
            "user_passwd": forms.PasswordInput(attrs={"class": "input_t",
                                                      "id": "user_passwd",
                                                      "name": "user_passwd",
                                                      "placeholder": "请输入密码",
                                                      "render_value": True}),
            "user_name": forms.TextInput(attrs={"class": "input_t",
                                                "id": "user_name",
                                                "name": "user_name",
                                                "placeholder": "请输入姓名"})
        }

    # 验证号码是否已存在
    def clean_user_num(self):
        number = self.cleaned_data["user_num"]
        number_models = NewUserInfo.objects.filter(user_num=number).exists()
        if number_models:
            raise ValidationError("注册号码已存在，请直接登录")
        else:
            return number

    # 密码进行加密
    def clean_user_passwd(self):
        user_passwd = md5(self.cleaned_data["user_passwd"])
        return user_passwd

    # 两次密码进行验证
    def clean_confirm_password(self):
        text_password = self.cleaned_data["user_passwd"]
        text_confirm_password = md5(self.cleaned_data["confirm_password"])
        if text_password != text_confirm_password:
            raise ValidationError("输入两次密码不匹配")
        return text_confirm_password
