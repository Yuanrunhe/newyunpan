#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# version: v1.0
# author : 袁润和
# Project : ythWhleProject
# File : yunpan.py
# Software: PyCharm
# time: 2023/4/24 22:41
"""
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse, Http404, FileResponse
from projectManagement.Form.Form import UploadFolderForm
from projectManagement.models import yunpan_first, yunpan_second, yunpan_third
from django.core.serializers.json import DjangoJSONEncoder
from newyunpan.models import NewUserInfo
from projectManagement.utils.authUser import User_auth

Symbol_file_type = {
    "YSB": "#icon-file-zip-fill",
    "PDF": "#icon-pdf",
    "WORD": "#icon-word",
    "EXCEL": "#icon-excel",
    "PPT": "#icon-ppt",
    "txt": "#icon-TXT",
    "folder": "#icon-wenjianjia",
    "es": "#icon-wenjianleixing-suolvetu-weizhiwenjian"
}


def pd_file_type(file_object):
    if file_object.content_type in ['application/zip', 'application/x-rar-compressed',
                                    'application/x-7z-compressed', 'application/x-tar',
                                    'application/gzip', 'application/x-bzip2']:
        file_type_2 = "YSB"
    elif file_object.content_type == 'application/pdf':
        file_type_2 = "PDF"
    elif file_object.content_type in ['application/msword',
                                      'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
        file_type_2 = "WORD"
    elif file_object.content_type in ['application/vnd.ms-excel',
                                      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:
        file_type_2 = "EXCEL"
    elif file_object.content_type in ['application/vnd.ms-powerpoint',
                                      'application/vnd.openxmlformats-officedocument.presentationml.presentation']:
        file_type_2 = "PPT"
    elif file_object.content_type == 'text/plain':
        file_type_2 = "txt"
    elif file_object.name.split('.')[-1] in ['zip', 'rar', 'Z', 'z', 'gzip', 'tar']:  # 放到最后判断
        file_type_2 = "YSB"
    else:
        file_type_2 = "es"

    return file_type_2


def yunpan(request):
    return render(request, "yunpan.html")


def add_folder(request):
    """
    添加文件，请求参数：
       folderName： 上传的文件夹名称，
       directory： 文件夹下所有文件，这里呢如果文件夹里面还有文件夹，那么不会取，只会将里面所有文件合并成一个级别的文件
       add_ccId： 这个是当前的上传文件的层次，字符串类型，用来判断当前的层次。因为最后一级是不包含的，所有在下面逻辑
                  会去掉最后一层。
       up_level： 表示上一层文件夹的ID，这里的ID是点前页面的上一层的，
    """

    user_auto = User_auth(request)
    user_object = user_auto.get_model()
    fkID = user_auto.fkID()

    response = {'syb_type': Symbol_file_type}
    if request.method == "POST":
        form = UploadFolderForm(request.POST, request.FILES)
        if form.is_valid():
            Folder_name = request.POST['folderName']  # 文件夹名称
            uploaded_files = request.FILES.getlist('directory')  # 获取文件列表
            add_ccId = request.POST.get("add_ccId", 0)  # 获取层次ID

            # 根据当前的上传层次来判断上一层和本层的models
            if add_ccId == "1":
                yunpan_model1 = yunpan_first.objects
                yunpan_model2 = yunpan_second.objects
            elif add_ccId == "2":
                yunpan_model1 = yunpan_second.objects
                yunpan_model2 = yunpan_third.objects
            elif add_ccId == "3":
                yunpan_model1 = 0
                yunpan_model2 = yunpan_third.objects
            else:
                raise Http404("上传失败")

            # 判断如果当前id大于等于2，那么就得获取上一层文件夹的ID
            if int(add_ccId) >= 2:
                up_level = request.POST.get("up_level", 0)  # 单层次大于2时页面会传输上一层的ID
                if int(up_level) == 0:
                    raise Http404("请求失败")
            else:
                up_level = 0

            # 第一层保存，因为表结构不一样就要多层判断，还有就是第三层(最后一层)只能存放文件，不能存放文件夹
            # 这里的new_yunpan_first_id是上一层的文件夹ID
            if yunpan_model1 != 0 and add_ccId == "1":
                new_yunpan_first = yunpan_model1.create(file_name=Folder_name, file_type=1,
                                                        person=user_object.name,
                                                        file_type_2="folder",
                                                        person_ID=fkID)
                new_yunpan_first_id = new_yunpan_first.id
            elif add_ccId == "2":
                up_level_pk = yunpan_first.objects.get(id=int(up_level))
                new_yunpan_first = yunpan_model1.create(file_name=Folder_name, file_type=1,
                                                        person=user_object.name,
                                                        file_type_2="folder", ParentID_1=up_level_pk,
                                                        person_ID=fkID)
                new_yunpan_first_id = new_yunpan_first.id
            else:
                # 最后一层因为没有文件夹，自取文件，所以这一层的id应该取上一层的ID
                new_yunpan_first_id = yunpan_second.objects.get(id=int(up_level)).id
                # 第二层保存
            for uploaded_file in uploaded_files:
                try:
                    file_name = uploaded_file.name if len(uploaded_file.name) <= 32 else uploaded_file.name[0:32]
                    if int(add_ccId) == 1:
                        file_type_2 = pd_file_type(uploaded_file)  # 获取文件类型
                        yunpan_model2.create(file_name=file_name, file=uploaded_file, file_type=2,
                                             person=user_object.name,
                                             ParentID_1_id=new_yunpan_first_id,
                                             file_type_2=file_type_2,
                                             person_ID=fkID)
                    if int(add_ccId) >= 2:
                        file_type_2 = pd_file_type(uploaded_file)  # 获取文件类型
                        yunpan_model2.create(file_name=file_name, file=uploaded_file, file_type=2,
                                             person=user_object.name,
                                             ParentID_1_id=new_yunpan_first_id, file_type_2=file_type_2,
                                             person_ID=fkID)
                except Exception as e:
                    print(f'Error: {e}')
                    raise Http404("请求失败")

            response['success'] = "success"
            return JsonResponse(response)
        else:
            response['err'] = "上传失败"
            return JsonResponse(response)
    else:
        form = UploadFolderForm()
        # 将 ModelForm 渲染为 HTML 表单
        form_html = render(request, "add_folder_model.html", {"form": form}).content
        return HttpResponse(form_html)


# 获取第一层的页面
def get_first_yunpan(request):
    user_auto = User_auth(request)
    user_object = user_auto.get_model()
    fkID = user_auto.fkID()

    datas = yunpan_first.objects.filter(person_ID=user_object.user_id).all()
    response = {}
    data_dict = []
    for data in datas:
        data_dict.append(
            {"id": data.id, "file_name": data.file_name,
             "file_type": data.file_type, "person": data.person,
             "file_type_2": data.file_type_2})
    response['data'] = data_dict
    response['file_type'] = Symbol_file_type
    return JsonResponse(response, safe=False)


# 获取第二层的页面
def get_second_yunpan(request):
    user_auto = User_auth(request)
    user_object = user_auto.get_model()
    fkID = user_auto.fkID()


    if request.method == "POST":
        pk = request.POST.get("id", "0")
        pk_first_object = yunpan_first.objects.filter(id=pk, person_ID=user_object.user_id).first()
        response = {}
        if pk_first_object:
            datas = pk_first_object.yunpan_second_set.all()  # 方向查询，关联外键表小写并加上_set
            data_dict = []
            for data in datas:
                data_dict.append(
                    {"id": data.id,
                     "file_name": data.file_name,
                     "file_type": data.file_type,
                     "file_type_2": data.file_type_2,
                     "person": data.person
                     }
                )
            response["data"] = data_dict
            response["file_type"] = Symbol_file_type
            response["success"] = "请求成功"
            response["up_level"] = pk  # 上一级的Id
            return JsonResponse(response, encoder=DjangoJSONEncoder, safe=False)

        else:
            response["error"] = "请求失败"
            return JsonResponse(response)
    else:
        return Http404("请求失败")


# 获取第二层的页面
def get_third_yunpan(request):
    user_auto = User_auth(request)
    user_object = user_auto.get_model()
    fkID = user_auto.fkID()

    if request.method == "POST":
        pk = request.POST.get("id", "0")
        pk_first_object = yunpan_second.objects.filter(id=pk, person_ID=user_object.user_id).first()
        response = {}
        if pk_first_object:
            datas = pk_first_object.yunpan_third_set.all()  # 方向查询，关联外键表小写并加上_set
            data_dict = []
            for data in datas:
                data_dict.append(
                    {"id": data.id,
                     "file_name": data.file_name,
                     "file_type": data.file_type,
                     "file_type_2": data.file_type_2,
                     "person": data.person
                     }
                )
            response["data"] = data_dict
            response["file_type"] = Symbol_file_type
            response["success"] = "请求成功"
            response["up_level"] = pk  # 上一级的Id
            return JsonResponse(response, encoder=DjangoJSONEncoder, safe=False)

        else:
            response["error"] = "请求失败"
            return JsonResponse(response)
    else:
        return Http404("请求失败")


# 创建文件夹
def create_folder(request):
    """
    请求参数
        btnId ：当前创建的层次
        inputValue ： 创建的文件夹


    :param request:
    :return:
    """

    user_auto = User_auth(request)
    user_object = user_auto.get_model()
    fkID = user_auto.fkID()

    response = {}

    if request.method == "POST":
        leve_id = request.POST.get("btnId", "0")  # 当前层次
        folder_name = request.POST.get("inputValue", " ")  # 文件名
        up_folder_id = request.POST.get("ccID", 0)  # 获取上一层id
        if leve_id == 0 or folder_name == " ":
            return Http404
        if leve_id == "1":
            model_object = yunpan_first.objects
        elif leve_id == "2":
            model_object = yunpan_second.objects
            if up_folder_id == 0:
                return Http404("创建失败")
            up_level_folder_id = yunpan_first.objects.filter(id=int(up_folder_id)).first().id
        else:
            return Http404("创建失败")
        try:
            if leve_id == "1":
                new_yunpan_model = model_object.create(file_name=folder_name, file_type=1,
                                                       person=user_object.name,
                                                       file_type_2="folder",
                                                       person_ID=fkID)
            else:
                new_yunpan_model = model_object.create(file_name=folder_name, file_type=1,
                                                       person=user_object.name,
                                                       file_type_2="folder", ParentID_1_id=up_level_folder_id,
                                                       person_ID=fkID)

            folder_id = new_yunpan_model.id
            response['success'] = "创建成功"
            response['folder_id'] = folder_id
            response['folder_name'] = folder_name
        except Exception as e:
            print(e)
            response['error'] = "创建失败"

        return JsonResponse(response, safe=False)


def load_file(request):
    user_auto = User_auth(request)
    user_object = user_auto.get_model()
    fkID = user_auto.fkID()

    re = {}
    if request.method == "GET":
        leve = request.GET.get("leve", None)
        _id = request.GET.get("id", None)
        session_name = user_object.name
        if not _id:
            raise Http404
        if leve:
            if int(leve) == 2:
                model_name = yunpan_second
            elif int(leve) == 3:
                model_name = yunpan_third
            else:
                re["error"] = "文件未找到"
                return JsonResponse(re)
        else:
            raise Http404
        file_object = model_name.objects.filter(id=int(_id), person_ID=user_object.user_nub).first()
        if file_object:
            if session_name != file_object.person:
                raise Http404
            try:
                file_name = str(file_object.file.path).split("\\")[-1]
                file = open(file_object.file.path, 'rb')
                response = FileResponse(file)
                response['Content-Type'] = 'application/octet-stream'
                response['Content-Disposition'] = f'attachment; filename="{file_name}"'.encode('utf-8', 'ISO-8859-1')
                return response
            except Exception as e:
                print(e)
                return HttpResponse("下载失败")
        else:
            raise Http404


def del_file(request):
    user_auto = User_auth(request)
    user_object = user_auto.get_model()
    fkID = user_auto.fkID()

    re = {}
    if request.method == "GET":
        leve = request.GET.get("leve", None)
        _id = request.GET.get("id", None)
        session_name = user_object.name
        if not _id:
            raise Http404
        if leve:
            if int(leve) == 2:
                model_name = yunpan_second
            elif int(leve) == 3:
                model_name = yunpan_third
            else:
                re["error"] = "文件未找到"
                return JsonResponse(re)
        else:
            raise Http404
        file_object = model_name.objects.filter(id=int(_id), person_ID=user_object.user_nub).first()
        if file_object:
            if session_name != file_object.person:
                raise Http404
            file_object.delete()
            return redirect("/yunpan/")
        else:
            raise Http404
