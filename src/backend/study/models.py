'''
study应用数据模型
'''
from django.db import models
from books.models import Category, UnitInfo, Word
from information.models import Student

class WordLog(models.Model):
    '''
    单词记录表
    '''
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey('information.Student', on_delete=models.CASCADE)
    category = models.ForeignKey('books.Category', on_delete=models.CASCADE)
    word = models.ForeignKey('books.Word', on_delete=models.CASCADE)
    unit = models.ForeignKey('books.UnitInfo', on_delete=models.CASCADE)
    unit_num = models.IntegerField()
    status = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    study_date = models.DateField()

class Question(models.Model):
    '''
    题目表
    '''
    id = models.AutoField(primary_key=True)
    word = models.ForeignKey('books.Word', on_delete=models.CASCADE)
    question_type = models.CharField(max_length=256)
    question = models.CharField(max_length=256)
    question_difficulty = models.CharField(max_length=256)
    correct_option = models.CharField(max_length=256)
    disturbance_option1 = models.CharField(max_length=256)
    disturbance_option2 = models.CharField(max_length=256)
    disturbance_option3 = models.CharField(max_length=256)

class StudyLog(models.Model):
    '''
    学习记录表
    '''
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey('information.Student', on_delete=models.CASCADE)
    study_date = models.DateField()
    study_duration = models.IntegerField(default=0)
    coin_number = models.IntegerField(default=0)

class TestLog(models.Model):
    '''
    测试记录表
    '''
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey('information.Student', on_delete=models.CASCADE)
    book = models.ForeignKey('books.Category', on_delete=models.CASCADE)
    test_type = models.CharField(max_length=256)
    test_time = models.DateTimeField()
    test_score = models.IntegerField(default=0)
    is_pass = models.BooleanField(default=False)

class PretestLog(models.Model):
    '''
    学前测试记录表
    '''
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    student = models.ForeignKey('information.Student', on_delete=models.CASCADE)
    book = models.ForeignKey('books.Category', on_delete=models.CASCADE)

class StudentUnit(models.Model):
    '''
    学生单元关联表
    '''
    id = models.AutoField(primary_key=True)
    unit = models.ForeignKey('books.UnitInfo', on_delete=models.CASCADE)
    unit_num = models.IntegerField()
    category = models.ForeignKey('books.Category', on_delete=models.CASCADE)
    student = models.ForeignKey('information.Student', on_delete=models.CASCADE)
    status = models.CharField(max_length=32, default='beforelearning')

class StudentBook(models.Model):
    '''
    学生课程关联表
    '''
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey('information.Student', on_delete=models.CASCADE)
    book = models.ForeignKey('books.Category', on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
