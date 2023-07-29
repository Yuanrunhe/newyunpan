#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# version: v1.0
# author : 袁润和
# Project : ythWhleProject
# File : pagep.py
# Software: PyCharm
# time: 2023/4/17 23:02
"""
import copy
from django.utils.safestring import mark_safe


class Paginstion(object):
    def __init__(self, requests, query_object, max_data=10, max_page=3, method="GET", paga_param="page",
                 dis_param=None, root=True):
        """
        获取分页组件的脚本
        get_html(self): 获取分页的html
        get_urlparam(self, page=None): 拼接分页标签的url参数
        get_data(self): 获取当前页面的数据对象

        :param requests: 请求的对象
        :param query_object: model对象
        :param max_data: 页面数据显示最大的函数
        :param max_page:  分页器当前页面前后的选项，默认3
        :param method: 请求类型，默认为get
        :param paga_param: url中当前页码的参数
        :param dis_param: url中需剔除的参数，列表形式出现
        :param root : 是否加上权限管理
        """

        self.requests = requests
        self.query_object = query_object
        self.max_data = max_data
        self.max_page = max_page
        self.dis_param = dis_param
        self.paga_param = paga_param
        self.method = method
        self.root = root
        if self.root:
            self.person = self.requests.session.get("info")["user_name"]
            self.user_id = self.requests.session.get("info")["user_id"]
            self.total = self.query_object.objects.filter(person=self.person, person_ID=self.user_id).all().count()
        else:
            self.total = self.query_object.objects.all().count()
        self.url_path = self.requests.path


        # 根据数据量获取总页码
        self.total_page = divmod(self.total, self.max_data)[0] + 1 if divmod(self.total, self.max_data)[1] else \
            divmod(self.total, self.max_data)[0]

        # 获取当前页码
        if method == "GET":
            self.page = requests.GET.get(self.paga_param, "1")
        else:
            self.page = requests.POST.get(self.paga_param, "1")
        if self.page.isdecimal():
            self.page = int(self.page)
        else:
            self.page = 1

        # 避免当前页面小于1或者大于总数
        if self.page > self.total_page:
            self.page = self.total_page
        elif self.page < 1:
            self.page = 1

        # # 取当前页码的前后个数
        if self.total_page <= self.max_page:
            self.start_page = 1
            self.end_page = self.total_page
        elif self.page < 1:
            self.start_page = 1
            self.end_page = (self.max_page * 2 + 1) if (self.max_page * 2 + 1) <= self.total_page else self.total_page
        elif self.page >= self.total_page:
            self.start_page = self.total_page - (self.max_page * 2) if (self.total_page - (
                    self.max_page * 2)) > 0 else 1
            self.end_page = self.total_page
        else:
            if self.page >= (self.total_page - self.max_page):
                if (self.total_page - (self.max_page * 2)) > 0:
                    self.start_page = self.total_page - (self.max_page * 2)
                else:
                    self.start_page = 1
                if (self.page + self.max_page) <= self.total_page:
                    self.end_page = self.page + self.max_page
                else:
                    self.end_page = self.total_page
            elif (self.page - self.max_page) <= 1:
                if self.total > (1 + (self.max_page * 2)):
                    self.start_page = 1
                    self.end_page = 1 + (self.max_page * 2)
                else:
                    self.start_page = 1
                    self.end_page = self.total_page
            else:
                self.start_page = self.page - self.max_page
                self.end_page = self.page + self.max_page

        self.page_str_list = []

    def get_html(self):
        """
        获取分页组件的html
        :return: html
        """

        # 设置首页按钮
        self.page_str_list.append(
            '<li><a href="{}?{}"><span aria-hidden="true">首页</span></a></li>'.format(
                self.url_path, self.get_urlparam(1)))
        # 获取上一页按钮
        if self.page == 1:
            self.page_str_list.append(
                '<li class="disabled"><a href="#"><span aria-hidden="true">&laquo;</span></a></li>')
        else:
            self.page_str_list.append(
                '<li><a href="{}?{}"><span aria-hidden="true">&laquo;</span></a></li>'.format(
                    self.url_path, self.get_urlparam(self.page - 1)))

        # 中间数据的按钮
        for page in range(self.start_page, self.end_page + 1):
            if page == self.page:
                self.page_str_list.append(
                    '<li class="active"><a href="{}?{}">{}</a></li>'.format(self.url_path, self.get_urlparam(page),
                                                                            page)
                )
            else:
                self.page_str_list.append(
                    '<li><a href="{}?{}">{}</a></li>'.format(self.url_path, self.get_urlparam(page), page)
                )

        # 获取下一页按钮
        if self.page == self.total:
            self.page_str_list.append(
                '<li class="disabled"><a href="#"><span aria-hidden="true">&raquo;</span></a></li>')
        else:
            self.page_str_list.append(
                '<li><a href="{}?{}"><span aria-hidden="true">&raquo;</span></a></li>'.format(
                    self.url_path, self.get_urlparam(self.page + 1)))
        # 获取尾页按钮
        self.page_str_list.append(
            '<li><a href="{}?{}"><span aria-hidden="true">尾页</span></a></li>'.format(
                self.url_path, self.get_urlparam(self.total_page)))
        page_string = mark_safe("".join(self.page_str_list))
        return page_string

    # 获取url参数,并且给定参数拼接
    def get_urlparam(self, page=None):
        """
        根据给定的页码拼接url的get参数
        :param page: 页码
        :return: url.get参数
        """
        if self.paga_param:
            url_param = copy.deepcopy(self.requests.GET)
            url_param._mutable = True
            # 先去除页码的当前页面参数，方便给生成html的拼接url
            url_param.pop(self.paga_param, None)
            # 去除指定的参数
            if self.dis_param:
                if isinstance(self.dis_param, list):
                    for i in page:
                        url_param.pop(i, None)
                else:
                    print("输入参数类型非列表")
            url_param.setlist(self.paga_param, [page])
            return url_param.urlencode()

    # 获取当前页面数据
    def get_data(self):
        """
        获取当前页的数据
        :return: data.objects
        """
        if self.total:
            start_data = (self.page - 1) * self.max_data
            end_data = self.page * self.max_data

            if self.root:
                data = self.query_object.objects.filter(person=self.person).all()[start_data: end_data]
            else:
                data = self.query_object.objects.all()[start_data: end_data]
        else:
            data = None
        return data
