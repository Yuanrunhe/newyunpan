#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# version: v1.0
# author : 袁润和
# Project : ythWhleProject
# File : login.py
# Software: PyCharm
# time: 2023/5/7 1:08
"""
from django.shortcuts import render, HttpResponse, redirect, Http404
from projectManagement.Form.ModelForm import login_modelform, register_modelform
from projectManagement.models import user_info
from datetime import datetime
from projectManagement.utils import redisBK
from newyunpan.models import NewUserInfo


def login(request):
    if request.method == "GET":
        mf = login_modelform()
        return render(request, "login.html", {"form": mf})
    else:
        re_mf = login_modelform(request.POST)
        if re_mf.is_valid():
            user_log = NewUserInfo.objects.filter(**re_mf.cleaned_data).first()
            re_code = request.POST.get("captcha", None)  # 前端输入验证码
            code_key = request.session.get("image_code")
            redis_code = redisBK.get_dict_value(code_key)  # redis保存的验证码
            if user_log:
                if re_code and redis_code:
                    if re_code.lower() != redis_code.lower():
                        return render(request, "login.html", {"form": re_mf, "yzm": "验证码不正确"})
                    request.session["info"] = {'user_id': user_log.user_id,
                                               'user_num': user_log.user_num,
                                               "user_name": user_log.user_name,
                                               "user_passwd": user_log.user_passwd,
                                               "user_group_id": user_log.user_group_id.group_id
                                               }
                    request.session["dl_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 登录时间
                    request.session.set_expiry(60 * 60 * 24)  # 设置session过期时间
                    del request.session['image_code']
                    # return redirect("/")
                    return redirect("/newyp/")
                else:
                    return render(request, "login.html", {"form": re_mf, "yzm": "验证码过期"})
            else:
                re_mf.add_error("user_passwd", "账号密码不存在")
                return render(request, "login.html", {"form": re_mf})

        return HttpResponse("验证失败")


def register(request):
    Register_Options = True
    if not Register_Options:
        return HttpResponse("<span style='color: red; font-size:20px;'>注册功能暂时关闭，请联系管理员开启账号,"
                            "<a href='/login/'>跳转回登录界面...</a></span>")

    if request.method == "GET":
        mf = register_modelform()
        return render(request, "register.html", {"form": mf})
    else:
        re_mf = register_modelform(request.POST)
        if re_mf.is_valid():
            article = re_mf.save(commit=False)
            now = datetime.now().strftime("%Y-%m-%d")
            article.change_passwd_time = now  # 最近一次修改密码时间
            article.save()
            return redirect("/login/", {"suc": "注册成功"})
        else:
            return HttpResponse("注册失败")


def log_off(request):
    request.session.clear()
    return redirect('/login/')
