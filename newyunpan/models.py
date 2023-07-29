from django.db import models
from django.utils import timezone


# Create your models here.

class UserGroup(models.Model):
    group_id = models.AutoField(primary_key=True, verbose_name="组ID")
    group_name = models.CharField(max_length=64, null=False, blank=False, verbose_name="组名")
    group_create_time = models.DateTimeField(default=timezone.now, verbose_name="创建时间")

    class Meta:
        db_table = 'user_group'


class NewUserInfo(models.Model):
    user_id = models.AutoField(primary_key=True, verbose_name="用户ID")
    user_name = models.CharField(max_length=64, null=False, blank=False, verbose_name="用户名")
    user_num = models.CharField(max_length=16, null=False, blank=False, verbose_name="用户号码")
    user_passwd = models.CharField(max_length=64, null=False, blank=False, verbose_name="用户密码")
    user_group_id = models.ForeignKey(UserGroup, to_field='group_id', on_delete=models.SET(1),
                                      default=1, verbose_name="关联组")
    userLevel_CHOICES = [
        ('1', '高级管理员'),
        ('2', '组管理员'),
        ('3', '普通用户'),
    ]
    user_level = models.CharField(max_length=1, choices=userLevel_CHOICES, default='3', verbose_name='用户类型')
    user_his_passwd = models.CharField(max_length=254, null=True, blank=True, verbose_name="历史密码")
    user_create_time = models.DateTimeField(default=timezone.now, verbose_name="创建时间")
    change_passwd_time = models.DateTimeField(default=timezone.now, verbose_name="最近一次修改密码时间")

    class Meta:
        db_table = 'new_user_info'


class FolderBook(models.Model):
    folder_id = models.AutoField(primary_key=True, verbose_name="文件夹ID")
    folder_name = models.CharField(max_length=128, null=False, blank=False, verbose_name="文件夹名")
    folder_group_id = models.ForeignKey(UserGroup, to_field='group_id', on_delete=models.CASCADE,
                                        verbose_name="关联组")
    folder_user_id = models.ForeignKey(NewUserInfo, to_field='user_id', on_delete=models.CASCADE,
                                       verbose_name="关联用户")
    folder_fk_id = models.ForeignKey('self', on_delete=models.CASCADE, to_field='folder_id', null=True, blank=True,
                                     verbose_name="文件上级关联")  # 默认为第一层
    folder_create_time = models.DateTimeField(default=timezone.now, verbose_name="创建时间")

    class Meta:
        db_table = 'folder_book'


class FileBook(models.Model):
    file_id = models.AutoField(primary_key=True, verbose_name="文件ID")
    file_path = models.FileField(verbose_name="文件路径", upload_to='newYunPan/%Y/%m/%d/', null=False, blank=False, default="unknown")
    file_name = models.CharField(max_length=128, null=False, blank=False, verbose_name="文件名")
    file_type = models.CharField(max_length=128, null=True, blank=True, default="unknown", verbose_name="文件类型")
    file_size = models.IntegerField(null=False, blank=False, default=0, verbose_name="文件大小")
    file_group_id = models.ForeignKey(UserGroup, to_field='group_id', on_delete=models.CASCADE,
                                      verbose_name="关联组")
    file_user_id = models.ForeignKey(NewUserInfo, to_field='user_id', on_delete=models.CASCADE,
                                     verbose_name="关联用户")
    file_folder_id = models.ForeignKey(FolderBook, to_field='folder_id', on_delete=models.CASCADE,
                                       verbose_name="关联文件夹")
    file_create_time = models.DateTimeField(default=timezone.now, verbose_name="创建时间")

    class Meta:
        db_table = 'File_book'
