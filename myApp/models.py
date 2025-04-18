from django.db import models

# Create your models here.
class User(models.Model):#用户表构建
    id = models.AutoField('id',primary_key=True)
    username = models.CharField('用户名',max_length=255,default='')
    password = models.CharField('密码',max_length=255,default='')
    createTime=models.DateTimeField('创建时间',auto_now_add=True)

    class Meta:
        db_table = 'user'

