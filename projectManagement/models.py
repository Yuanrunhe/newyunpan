from django.db import models


# Create your models here.

class user_info(models.Model):
    user_nub = models.AutoField(primary_key=True, verbose_name="用户ID")
    number = models.CharField(max_length=11, null=False, blank=False, verbose_name="手机号")
    name = models.CharField(max_length=16, null=False, blank=False, verbose_name="姓名")
    password = models.CharField(max_length=64, null=False, blank=False, verbose_name="密码")
    reg_date = models.DateField(null=False, blank=False, verbose_name="注册时间")
    status_dict = {
        (1, "正常"),
        (2, "失效")
    }
    status = models.CharField(max_length=16, choices=status_dict, verbose_name="状态")
    limits_dict = {
        (1, "普通用户"),
        (2, "超级管理员")
    }
    limits = models.CharField(max_length=16, choices=limits_dict, verbose_name="账号权限")
    change_pwd_date = models.DateField(null=False, blank=False, verbose_name="最近一次修改密码时间")

    class Meta:
        db_table = "user_info"
        verbose_name = "用户表"


class project_info(models.Model):
    id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=32, null=False, blank=False, verbose_name="项目名称")
    person = models.CharField(max_length=16, null=False, blank=False, verbose_name="负责人")
    project_file = models.FileField(verbose_name="脚本路径", upload_to='project_file/%Y/%m/%d/')
    upload_date = models.DateField(null=False, blank=False, verbose_name="上传时间")
    person_ID = models.ForeignKey(to="user_info", to_field="user_nub", on_delete=models.CASCADE, verbose_name="上传人关联ID",
                                  default=1)
    change_date = models.DateField(null=True, blank=True, verbose_name="最近一次更改时间")
    remarks = models.CharField(max_length=128, null=True, blank=True, verbose_name="备注")

    class Meta:
        db_table = 'projrct_info'
        verbose_name = '项目信息表'


class MenuItem(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    url = models.URLField(null=True, blank=True)
    auth_dict = {
        (1, "普通用户"),
        (2, "超级管理员"),
        (3, "全部"),
    }
    auth = models.CharField(max_length=16, choices=auth_dict, verbose_name="权限", default=3)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'MenuItem'
        verbose_name = '菜单'


class note_info(models.Model):
    id = models.AutoField(primary_key=True)
    note_name = models.CharField(max_length=32, null=False, blank=False, verbose_name="笔记名称")
    person = models.CharField(max_length=16, null=False, blank=False, verbose_name="负责人")
    note_file = models.FileField(verbose_name="笔记路径", upload_to='note_file/%Y/%m/%d/')
    upload_date = models.DateField(null=False, blank=False, verbose_name="上传时间")
    person_ID = models.ForeignKey(to="user_info", to_field="user_nub", on_delete=models.CASCADE, verbose_name="上传人关联ID",
                                  default=1)
    remarks = models.CharField(max_length=128, null=True, blank=True, verbose_name="备注")

    class Meta:
        db_table = 'note_info'
        verbose_name = '笔记管理表'


# 云盘
file_type_dict = {
    (1, "文件夹"),
    (2, "文件")
}


class yunpan_first(models.Model):
    id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=32, null=False, blank=False, verbose_name="文件名")
    file_type = models.CharField(max_length=32, choices=file_type_dict, verbose_name="文件类型")
    file_type_2 = models.CharField(max_length=32, verbose_name="详细文件类型")
    person = models.CharField(max_length=32, null=False, blank=True, verbose_name="上传人")
    person_ID = models.ForeignKey(to="user_info", to_field="user_nub", on_delete=models.CASCADE, verbose_name="上传人关联ID",
                                  default=1)

    class Meta:
        db_table = 'yunpan_first'
        verbose_name = '云盘一层模型'


class yunpan_second(models.Model):
    id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=32, null=False, blank=False, verbose_name="文件名")
    file = models.FileField(verbose_name="二级文件路径", upload_to='second_file/%Y/%m/%d/', null=True, blank=True)
    file_type = models.CharField(max_length=32, choices=file_type_dict, verbose_name="文件类型")
    file_type_2 = models.CharField(max_length=32, verbose_name="详细文件类型")
    person = models.CharField(max_length=32, null=False, blank=True, verbose_name="上传人")
    person_ID = models.ForeignKey(to="user_info", to_field="user_nub", on_delete=models.CASCADE, verbose_name="上传人关联ID",
                                  default=1)
    ParentID_1 = models.ForeignKey(to="yunpan_first", to_field='id', on_delete=models.CASCADE, verbose_name="一级关联")

    class Meta:
        db_table = 'yunpan_second'
        verbose_name = '云盘二层模型'


class yunpan_third(models.Model):
    id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=32, null=False, blank=False, verbose_name="文件名")
    file = models.FileField(verbose_name="三级文件路径", upload_to='third_file/%Y/%m/%d/', null=True, blank=True)
    file_type = models.CharField(max_length=32, choices=file_type_dict, verbose_name="文件类型")
    file_type_2 = models.CharField(max_length=32, verbose_name="详细文件类型")
    person = models.CharField(max_length=32, null=False, blank=True, verbose_name="上传人")
    person_ID = models.ForeignKey(to="user_info", to_field="user_nub", on_delete=models.CASCADE, verbose_name="上传人关联ID",
                                  default=1)
    ParentID_1 = models.ForeignKey(to="yunpan_second", to_field='id', on_delete=models.CASCADE, verbose_name="二级关联")

    class Meta:
        db_table = 'yunpan_third'
        verbose_name = '云盘三层模型'

