from django.db import models
from information.models import Student
from study.models import Question
from books.models import Category

class PKLog(models.Model):
    id = models.AutoField(primary_key=True)
    competition = models.ForeignKey('CompetitionInfo', on_delete=models.CASCADE)
    student = models.ForeignKey('information.Student', on_delete=models.CASCADE)
    question = models.ForeignKey('study.Question', on_delete=models.CASCADE)
    time = models.IntegerField()
    answer = models.CharField(max_length=256)
    is_right = models.BooleanField()

class InfiniteChallengeLog(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey('information.Student', on_delete=models.CASCADE)
    competition = models.ForeignKey('CompetitionInfo', on_delete=models.CASCADE)
    question = models.ForeignKey('study.Question', on_delete=models.CASCADE)
    is_right = models.BooleanField()

class CompetitionInfo(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    organiser = models.CharField(max_length=256)
    status = models.CharField(max_length=256)
    create_time = models.DateTimeField()
    begin_time = models.DateField()
    end_time = models.DateField()
    max_number = models.BigIntegerField()
    type = models.CharField(max_length=25)
    difficulty = models.CharField(max_length=25)
    tool = models.BooleanField(default=True)
    zn_to_en = models.BooleanField(default=False)
    en_to_zn = models.BooleanField(default=False)
    listen_to_spelling = models.BooleanField(default=False)
    listen_to_choose = models.BooleanField(default=False)
    coin_number = models.IntegerField(default=0)
    book_id = models.IntegerField()
    top_number = models.IntegerField()
    award = models.IntegerField()
    classes = models.CharField(max_length=256)
    school = models.CharField(max_length=256)
    grade = models.IntegerField()

class StudentHasCompetitionLog(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey('information.Student', on_delete=models.CASCADE)
    competition = models.ForeignKey('CompetitionInfo', on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    