#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# version: v1.0
# author : 袁润和
# Project : ythWhleProject
# File : noteview.py
# Software: PyCharm
# time: 2023/4/19 23:31
"""
from datetime import datetime
import codecs

# import markdown
import markdown2
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse, FileResponse, Http404
from projectManagement.Form.ModelForm import add_note_info
from projectManagement.models import note_info
from projectManagement.utils.paginstion import Paginstion
from projectManagement.utils.authUser import User_auth


def note_list(request):
    user_auto = User_auth(request)
    user_object = user_auto.get_model()
    fkID = user_auto.fkID()
    if request.method == "GET":
        note_data = add_note_info()
        paginstion = Paginstion(requests=request, query_object=note_info)
        response = {
            "data": paginstion.get_data(),
            "form": note_data,
            "html": paginstion.get_html()
        }
        return render(request, "note_list.html", response)


def add_note(request):
    user_auto = User_auth(request)
    user_object = user_auto.get_model()
    fkID = user_auto.fkID()

    response = {}
    if request.method == "POST":
        model_data = add_note_info(request.POST, request.FILES)
        if model_data.is_valid():
            response['success'] = "添加成功"
            article = model_data.save(commit=False)
            # 获取当前日期和时间
            now = datetime.now()
            date_str = now.strftime("%Y-%m-%d")
            article.upload_date = date_str
            article.person = user_object.name
            article.person_ID = fkID
            article.save()
        else:
            response['err'] = "添加失败,请确保没空值及文件大小不超20M"

        return JsonResponse(response)


def load_note(request, nid):
    user_auto = User_auth(request)
    user_object = user_auto.get_model()
    fkID = user_auto.fkID()

    file_object = note_info.objects.filter(id=nid, person_ID=user_object.user_nub).first()

    if file_object:
        try:
            file_name = str(file_object.note_file.path).split("\\")[-1]
            file = open(file_object.note_file.path, 'rb')
            response = FileResponse(file)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'.encode('utf-8', 'ISO-8859-1')
            return response
        except Exception:
            raise Http404


def del_note(request):
    user_auto = User_auth(request)
    user_object = user_auto.get_model()
    fkID = user_auto.fkID()

    pk = request.POST.get("id")
    file_object = note_info.objects.filter(id=pk, person_ID=user_object.user_nub).first()
    response = {}
    if file_object:
        file_object.delete()
        response['success'] = "删除成功"
        return JsonResponse(response)
    else:
        response["err"] = "删除失败"
        return Http404


def note_view(request):
    user_auto = User_auth(request)
    user_object = user_auto.get_model()
    fkID = user_auto.fkID()

    _id = request.GET.get("id", "0")
    response = {}
    if _id != "0":
        note_project = note_info.objects.filter(id=_id, person_ID=user_object.user_nub).first()
        if note_project:
            path = note_project.note_file.path
            file_name = path.split("\\")[-1]
            file_type = file_name.split(".")[1] if len(file_name.split(".")) > 1 else "txt"
            response['file_name'] = file_name
            if file_type == "md":
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                html_content = markdown2.markdown(content).replace("````", "```").replace("`````", "```")
                response['content'] = html_content
                print(content)
            else:
                with open(path, 'rb') as f:
                    content = codecs.decode(f.read(), 'utf-8', errors='ignore')
                    response['content'] = content
            response['filetype'] = file_type
            return render(request, "note_view.html", {"response": response})
        else:
            return HttpResponse("请求失败")

    return HttpResponse("请求失败")
