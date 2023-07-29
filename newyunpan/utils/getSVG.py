#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# version: v1.0
# author : 袁润和
# Project : ythWhleProject
# File : getSVG.py
# Software: PyCharm
# time: 2023/7/20 22:39
"""

def getSVG(typeTile):
    allType = {"image": "#icon-file_img",
               "audio": "#icon-audio",
               "video": "#icon-video",
               "text/plain": "#icon-TXT",
               "html": "#icon-html",
               "css": "#icon-css",
               "javascript": "#icon-javascript",
               "zip": "#icon-zip",
               "rar": "#icon-RARtubiao",
               "7z": "#icon-Ztubiao",
               "tar": "#icon-TAR",
               "pdf": "#icon-pdf",
               "word": "#icon-word",
               "xml": "#icon-xml",
               "excel": "#icon-excel",
               "powerpoint": "#icon-ppt",
               "ppt": "#icon-ppt",
               "csv": "#icon-csv",
               "json": "#icon-json",
               "font": "#icon-font",
               "java": "#icon-a-ziyuan1",
               "python": "#icon-Python",
               "sh": "#icon-powershell",
               }
    unknow = "#icon-wenjianleixing-suolvetu-weizhiwenjian"
    for tyT in allType:
        if tyT in typeTile:
            return allType[tyT]
    return unknow
