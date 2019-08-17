from django.db import models

class UnitInfo(models.Model):
    unit_id = models.AutoField(primary_key=True)
    unit_num = models.IntegerField()
    book = models.ForeignKey('Category', on_delete=models.CASCADE)
    total_number = models.IntegerField()

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=512)
    create_time = models.CharField(max_length=512)
    modify_time = models.CharField(max_length=512)
    grade_id = models.IntegerField()
    enable = models.BooleanField()
    sequence = models.IntegerField()
    edition = models.ForeignKey('Edition', on_delete=models.CASCADE)
    cover_pic = models.CharField(max_length=256)

class Word(models.Model):
    id = models.AutoField(primary_key=True)
    word = models.CharField(max_length=128)
    explains = models.CharField(max_length=512)
    difficult = models.IntegerField()
    pronunciation = models.CharField(max_length=512)
    has_polyphone = models.BooleanField(default=False)
    create_time = models.CharField(max_length=512)
    modify_time = models.CharField(max_length=512)
    other_spelt = models.CharField(max_length=512)
    spelt_sound = models.CharField(max_length=512)
    type = models.IntegerField()
    junior_level = models.IntegerField()
    senior_level = models.IntegerField()

class Classification(models.Model):
    id = models.AutoField(primary_key=True)
    word = models.ForeignKey('Word', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    sequence = models.IntegerField()
    create_time = models.CharField(max_length=512)
    modify_time = models.CharField(max_length=512)
    gra_id = models.IntegerField()

class Edition(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=512, null=False)
    create_time = models.CharField(max_length=512)
    modify_time = models.CharField(max_length=512)
    unit_enable = models.BooleanField()

class ExampleSentence(models.Model):
    id = models.AutoField(primary_key=True)
    word = models.ForeignKey('Word', on_delete=models.CASCADE)
    example_sentence_ch = models.TextField()
    example_sentence_en = models.TextField()

class UnitWord(models.Model):
    id = models.AutoField(primary_key=True)
    unit = models.ForeignKey('UnitInfo', on_delete=models.CASCADE)
    word = models.ForeignKey('Word', on_delete=models.CASCADE)
