#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# version: v1.0
# author : 袁润和
# Project : ythWhleProject
# File : menu.py
# Software: PyCharm
# time: 2023/4/21 23:02
"""

from projectManagement.models import MenuItem
from django.http import JsonResponse


def menu(request):
    menu_items = MenuItem.objects.all()
    menu = {}
    for item in menu_items:
        if not item.parent:
            menu[item.id] = {
                'name': item.name,
                'url': item.url,
                'children': [
                ]
            }
        else:
            menu[item.parent.id]['children'].append({
                'name': item.name,
                'url': item.url

            })
    data = {
        'menu': menu,
    }
    print(data)
    return JsonResponse(data)
