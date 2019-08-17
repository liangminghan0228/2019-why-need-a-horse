'''
TeacherBuiltIn应用数据模型
'''
from django.db import models

class TeacherBuiltIn(models.Model):
    '''
    教师信息内置表
    '''
    username = models.CharField(max_length=128, primary_key=True)
    password = models.CharField(max_length=256)
