#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# version: v1.0
# author : 袁润和
# Project : ythWhleProject
# File : fast_jies.py
# Software: PyCharm
# time: 2023/5/13 21:57
"""
from django.shortcuts import render


def get_who(request):
    return render(request, "iswho.html")
