"""
URL configuration for ythWhleProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve
from django.conf import settings
from projectManagement.views import manage, menu, noteview, login, account, fast_jies

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', manage.projectManage),
    path('iswho/', fast_jies.get_who),

    # 登录
    path('login/', login.login),
    path('image/code/', account.image_code),
    path('register/', login.register),
    path('log_off/', login.log_off),

    # 项目列表
    path('projectList/', manage.projectList),
    path('add_project/', manage.add_project),
    path('edit_project/', manage.edit_project),
    path('load_project/<int:nid>', manage.load_project),
    path('del_project/', manage.del_project),

    # 菜单列表
    path('menu/', menu.menu, name='menu'),

    # 附件
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),

    # 笔记汇总
    path('noteList/', noteview.note_list),
    path('add_note/', noteview.add_note),
    path('load_note/<int:nid>', noteview.load_note),
    path('del_note/', noteview.del_note),
    path('note_view/', noteview.note_view),

    # 云盘
    path('yunpan/', include(('projectManagement.urls', 'yunpan'))),

    # 新云盘
    path('newyp/', include(('newyunpan.ypUrl', 'newyp'))),
]
