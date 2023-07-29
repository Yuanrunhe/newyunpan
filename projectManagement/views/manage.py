#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# version: v1.0
# author : 袁润和
# Project : ythWhleProject
# File : manage.py
# Software: PyCharm
# time: 2023/4/8 23:14
"""

from django.shortcuts import HttpResponse, redirect, render, get_object_or_404
from django.http import JsonResponse, FileResponse, Http404
from projectManagement.models import project_info, user_info
from projectManagement.Form.ModelForm import add_projrct_info, edit_project_info
from datetime import datetime
from projectManagement.utils.paginstion import Paginstion
from projectManagement.utils.authUser import User_auth


def projectManage(request):
    return render(request, "projectManage.html")


def projectList(request):
    user_auto = User_auth(request)
    user_object = user_auto.get_model()
    fkID = user_auto.fkID()

    if request.method == "GET":
        form = add_projrct_info()
        paginstion = Paginstion(request, project_info, max_data=10)
        html = paginstion.get_html()
        data = paginstion.get_data()
        response = {
            "alldata": data,
            "form": form,
            "html": html
        }
        return render(request, "project_list.html", response)


def add_project(request):
    user_auto = User_auth(request)
    user_object = user_auto.get_model()
    fkID = user_auto.fkID()

    if request.method == "POST":
        form = add_projrct_info(request.POST, request.FILES)
        # print(form.cleaned_data)
        if form.is_valid():
            article = form.save(commit=False)  # 创建一个Article对象但不保存到数据库中
            article.person = user_object.name  # 添加person属性
            # 获取当前日期和时间
            now = datetime.now()
            date_str = now.strftime("%Y-%m-%d")
            article.upload_date = date_str
            article.change_date = date_str
            article.person_ID = fkID
            article.save()  # 保存到数据库
            return JsonResponse({"suc": "True"})
        else:
            errors = {}
            for field, messages in form.errors.items():
                errors[field] = messages
            return JsonResponse({"errors": errors}, status=400)


# 修改未完善
def edit_project(request):
    user_auto = User_auth(request)
    user_object = user_auto.get_model()
    fkID = user_auto.fkID()

    if request.method == "GET":
        _id = request.GET.get('id')
        instance = project_info.objects.get(id=_id, person_ID=user_object.user_nub)
        form = edit_project_info(instance=instance)
        context = {'form': form.as_p()}
        return JsonResponse(context)
    elif request.method == "POST":
        form = edit_project_info(request.POST, request.FILES)
        if form.is_valid():
            return JsonResponse({'success': True})
        else:
            errors = {}
            for field, messages in form.errors.items():
                errors[field] = messages
            return JsonResponse({"errors": errors}, status=400)


def load_project(request, nid):
    user_auto = User_auth(request)
    user_object = user_auto.get_model()
    fkID = user_auto.fkID()

    file_object = project_info.objects.filter(id=nid, person_ID=user_object.user_nub).first()
    if file_object:
        try:
            file_name = str(file_object.project_file.path).split("\\")[-1]
            file = open(file_object.project_file.path, 'rb')
            response = FileResponse(file)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'.encode('utf-8', 'ISO-8859-1')
            return response
        except Exception:
            raise Http404


def del_project(request):
    user_auto = User_auth(request)
    user_object = user_auto.get_model()
    fkID = user_auto.fkID()

    if request.method == "POST":
        pk = request.POST.get("id")
        person = user_auto.get_person()  # 添加person属性
        data = project_info.objects.filter(id=pk, person_ID=user_object.user_nub).first()
        if data.person != person:
            response = {"error": "文件归属问题"}
            return JsonResponse(response)
        if data:
            data.delete()
            response = {"success": "删除成功"}
        else:
            response = {"error": "删除失败"}
        return JsonResponse(response)
    else:
        raise Http404
