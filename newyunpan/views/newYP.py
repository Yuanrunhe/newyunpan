#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# version: v1.0
# author : 袁润和
# Project : ythWhleProject
# File : newYP.py
# Software: PyCharm
# time: 2023/7/1 22:21
"""

from django.shortcuts import HttpResponse, redirect, render, get_object_or_404
from django.http import JsonResponse, FileResponse, Http404
from newyunpan.FORM.form import UploadFolderForm
from newyunpan.FORM.ModelForm import CreateFolder
from newyunpan.models import FolderBook, NewUserInfo, UserGroup, FileBook
from newyunpan.utils.getSVG import getSVG


def newyp(request):
    return render(request, "newYP.html")


def up_file_view(request):
    UserInfo = request.session.get("info")
    if request.method == 'GET':
        form = UploadFolderForm()
        form_html = render(request, "upfile.html", {"form": form}).content
        return HttpResponse(form_html)
    elif request.method == "POST":
        UserInfoObject = NewUserInfo.objects.get(user_id=UserInfo['user_id'], user_passwd=UserInfo['user_passwd'],
                                                 user_num=UserInfo['user_num'])
        uploaded_file = request.FILES['file']  # 获取上传的文件对象
        fileName = request.POST['filename']
        filetype = request.POST['fileType']
        fileSize = request.POST['fileSize']

        FileBookObject = FileBook()
        FileBookObject.file_path = uploaded_file
        FileBookObject.file_name = fileName
        FileBookObject.file_type = filetype
        FileBookObject.file_size = int(fileSize)
        FileBookObject.file_group_id = UserGroup.objects.get(group_id=UserInfo['user_group_id'])
        FileBookObject.file_user_id = UserInfoObject
        FileBookObject.file_folder_id = FolderBook.objects.get(folder_id=request.POST.get('levelID'))
        FileBookObject.save()

        return JsonResponse({'message': '文件上传成功'})


# 创建文件夹
def create_Folder(request):
    if request.method == 'GET':
        form = CreateFolder()
        form_html = render(request, "upfile.html", {"form": form}).content
        return HttpResponse(form_html)
    elif request.method == 'POST':
        FolderName = request.POST.get("folderName")
        FolderLevel = request.POST.get("folderLevel")
        UserID = request.session.get("info")['user_id']
        UserIDObjec = NewUserInfo.objects.get(user_id=UserID)
        FolderBookObject = FolderBook()
        FolderBookObject.folder_name = FolderName
        FolderBookObject.folder_group_id = UserIDObjec.user_group_id
        FolderBookObject.folder_user_id = UserIDObjec
        if FolderLevel == "file-first":
            FolderBookObject.save()
            return JsonResponse({'message': '创建成功',
                                 'Folder': FolderName},
                                status=200)
        else:
            folderLevel = request.POST.get('folderLevel')
            levelFolderIDObject = FolderBook.objects.get(folder_id=folderLevel)
            FolderBookObject.folder_fk_id = levelFolderIDObject
            FolderBookObject.save()
            return JsonResponse({'message': '创建成功',
                                 'Folder': FolderName},
                                status=200)
        # 需添加非第一层的

    return JsonResponse({'message': '创建失败'})


# 获取页面数据
def getPageFile(request):
    UserID = request.session.get("info")['user_id']
    UserIDObjec = NewUserInfo.objects.get(user_id=UserID)

    if request.method == "POST":
        FolderDict = {}
        FileDict = {}
        FolderLevel = request.POST.get("folderID")

        if FolderLevel == "file-first":
            FolderBookObject = FolderBook.objects.filter(folder_user_id=UserIDObjec, folder_fk_id__isnull=True). \
                values('folder_id', 'folder_name')
        else:
            FolderID = FolderBook.objects.get(folder_id=int(FolderLevel))
            FolderBookObject = FolderBook.objects.filter(folder_user_id=UserIDObjec, folder_fk_id=FolderID). \
                values('folder_id', 'folder_name')

        if FolderBookObject.exists():
            for FolderData in FolderBookObject:
                FolderDict[FolderData['folder_id']] = FolderData['folder_name']
        else:
            FolderDict = "None"

        # 第一层获取
        if FolderLevel == "file-first":
            FileDict = "None"
            return JsonResponse({'message': '获取成功',
                                 'FolderDict': FolderDict,
                                 'FileDict': FileDict}, status=200)
        FolderBookID = FolderBook.objects.get(folder_id=int(FolderLevel))  # 获取进来的文件夹ID
        FileBookObject = FileBook.objects.filter(file_user_id=UserIDObjec, file_folder_id=FolderBookID). \
            values('file_id', 'file_name', 'file_type')

        # 非第一次获取
        if FileBookObject.exists():
            for FileData in FileBookObject:
                firstFileDict = {
                    "fileName": FileData['file_name'],
                    "fileType": getSVG(FileData['file_type'])
                }
                # FileDict[FileData['file_id']] = FileData['file_name']
                # FileDict["fileType"] = getSVG(FileData['file_type'])
                FileDict[FileData['file_id']] = firstFileDict
        else:
            FileDict = "None"
        return JsonResponse({'message': '获取成功',
                             'FolderDict': FolderDict,
                             'FileDict': FileDict}, status=200)
    return JsonResponse({'message': '获取失败'}, status=400)


# 获取上一层页面的参数
def getrtupData(request):
    if request.method == "POST":
        levelID = request.POST.get("levelID")
        infoSeession = request.session.get("info")
        userObject = NewUserInfo.objects.get(user_id=infoSeession['user_id'], user_passwd=infoSeession['user_passwd'])
        datalevel = FolderBook.objects.get(folder_user_id=userObject, folder_id=levelID).folder_fk_id
        if datalevel:
            upFolder = datalevel.folder_id
        else:
            upFolder = "file-first"
        return JsonResponse({'message': '获取成功', 'upLevelID': upFolder}, status=200)
    return JsonResponse({'message': '获取失败'}, status=400)


# 下载
def fileDown(request):
    if request.method == "GET":
        try:
            fileID = request.GET.get('fileID')
            user_id = request.session.get('info')['user_id']
            pswd = request.session.get('info')['user_passwd']
            userObject = NewUserInfo.objects.get(user_id=user_id, user_passwd=pswd)
            if not userObject:
                return HttpResponse("无效用户,下载失败")
            fileObject = FileBook.objects.filter(file_id=int(fileID), file_user_id_id=user_id).first()
            file_name = str(fileObject.file_path.path).split("\\")[-1]
            file = open(fileObject.file_path.path, 'rb')
            response = FileResponse(file)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'.encode('utf-8', 'ISO-8859-1')
            return response
        except Exception as e:
            print(e)
            return HttpResponse("下载失败")
    return Http404


def deleteFile(request):
    if request.method == "POST":
        fileID = request.POST.get('fileID')
        user_id = request.session.get('info')['user_id']
        user_group_id = request.session.get('info')['user_group_id']
        FileBook_Object = FileBook.objects.filter(file_id=fileID, file_user_id_id=user_id, file_group_id_id=user_group_id)
        if FileBook_Object:
            FileBook_Object.delete()
            return JsonResponse({'message': '删除成功'}, status=200)
        return JsonResponse({'message': '删除失败'}, status=502)
    return Http404
