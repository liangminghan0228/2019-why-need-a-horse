'''
study应用数据模型
'''
from django.db import models

class StudentBuiltIn(models.Model):
    '''
    学生信息内置表
    '''
    password = models.CharField(max_length=256)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)

class Classes(models.Model):
    '''
    班级数据表
    '''
    id = models.AutoField(primary_key=True)
    classes_description = models.TextField()
    student_number = models.IntegerField(default=0)
    class_name = models.CharField(max_length=256)

class Student(models.Model):
    '''
    学生信息数据表
    '''
    id = models.CharField(max_length=128, primary_key=True)
    student_name = models.CharField(max_length=128)
    email = models.EmailField()
    login_times = models.IntegerField()
    coin_total = models.IntegerField(default=0)
    register_time = models.DateField()
    pay_status = models.BooleanField(default=False)
    classes = models.ForeignKey('Classes', on_delete=models.CASCADE)
    avatar = models.CharField(max_length=512)
    vocabularies = models.IntegerField(default=0)
    cumulative_study_duration = models.IntegerField(default=0)
    last_login = models.DateTimeField()
    grade = models.IntegerField()
    school = models.CharField(max_length=512)
