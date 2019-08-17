'''
该文件用于保存单元测试中常用函数，方便调用
'''
from django.utils import timezone
from django.test.client import Client
from django.test import TestCase
from books.models import *
from competitions.models import *
from information.models import *
from study.models import *
from teachers.models import *
import sys
sys.setrecursionlimit(100000)

def create_edition():
    if Edition.objects.filter(id=1).exists():
        return Edition.objects.get(id=1)
    else:
        edition_obj = Edition.objects.create(
        id=1,
        name='新高中课程',
        create_time='2019-08-15',
        modify_time='2019-08-16',
        unit_enable=True
        )
        return edition_obj



def create_category():
    if Category.objects.filter(id=1).exists():
        return Category.objects.get(id=1)
    else:
        category_obj = Category.objects.create(
        id=1,
        category='新高中课程',
        create_time='2019-08-15',
        modify_time='2019-08-15',
        grade_id=10,
        enable=True,
        sequence=1,
        edition=create_edition(),
        cover_pic='#'
        )
        return category_obj
def create_unit_info():
    if UnitInfo.objects.filter(unit_id=1).exists():
        return UnitInfo.objects.get(unit_id=1)
    else:
        unitInfo_obj = UnitInfo.objects.create(
        unit_id=1,
        unit_num=1,
        book=create_category(),
        total_number=4
        )
        return unitInfo_obj

def create_word():
    if Word.objects.filter(id=1).exists():
        return Word.objects.get(id=1)
    else:
        word_obj=Word.objects.create(
        id=1,
        word='hello',
        explains='你好',
        difficult=1,
        pronunciation='hello',
        has_polyphone=False,
        create_time='2019-08-15',
        modify_time='2019-08-15',
        other_spelt='null',
        spelt_sound='null',
        type=1,
        junior_level=1,
        senior_level=100
        )
        return word_obj

def create_classification():
    if Classification.objects.filter(id=1).exists():
        return Classification.get(id=1)
    else:
        classification_obj=Classification.objects.create(
        id=1,
        word=create_word(),
        category=create_category(),
        sequence=1,
        create_time='2019-08-15',
        modify_time='2019-08-15',
        gra_id=10
        )
        return classification_obj

def create_example_sentence():
    if ExampleSentence.objects.filter(id=1).exists():
        return ExampleSentence.objects.get(id=1)
    else:
        exampleSentence_obj=ExampleSentence.objects.create(
        id=1,
        word=create_example_sentence(),
        example_sentence_ch='中文例句',
        example_sentence_en='exampleSentence'
        )
        return exampleSentence_obj

def create_unit_word():
    if UnitWord.objects.filter(id=1).exists():
        return UnitWord.objects.get(id=1)
    else:
        unitWord_obj=UnitWord.objects.create(
        id=1,
        unit=create_unit_info(),
        word=create_word()
        )
        return unitWord_obj

def create_competitionInfo():
    if CompetitionInfo.objects.filter(id=1).exists():
        return CompetitionInfo.objects.get(id=1)
    else:
        competitionInfo_obj = CompetitionInfo.objects.create(
        id=1,
        name='pk',
        organiser='nku',
        status='abort',
        create_time='2019-08-16',
        begin_time='2019-08-16',
        end_time='2019-08-16',
        max_number=1000,
        type='pk',
        difficulty='easy',
        tool=True,
        zn_to_en=False,
        en_to_zn=True,
        listen_to_spelling=True,
        listen_to_choose=True,
        coin_number=100,
        book_id=1,
        top_number=3,
        award=50,
        classes=1,
        school='pkfour',
        grade=100
        )
        return competitionInfo_obj

def create_classes():
    if Classes.objects.filter(id=1).exists():
        return Classes.objects.get(id=1)
    else:
        classes_obj = Classes.objects.create(
        id=1,
        classes_description='class two',
        student_number=123,
        class_name='class two'
        )
        return classes_obj

def create_student():
    if Student.objects.filter(id='1'):
        return Student.objects.get(id='1')
    else:
        student_obj = Student.objects.create(
        id='1',
        student_name='tl',
        login_times=2019,
        coin_total=100,
        classes_id=create_classes(),
        register_time='2019-12-12',
        avatar='avatar',
        vocabularies=123,
        cumulative_study_duration=1234,
        last_login='2019-12-12 01:26',
        grade=3,
        school='NKU'
        )
        return student_obj

def create_student_has_competition_log():
    if StudentHasCompetitionLog.objects.filter(id=1).exists():
        return StudentHasCompetitionLog.objects.get(id=1)
    else:
        studentHasCompetition_obj = StudentHasCompetitionLog.objects.create(
        id=1,
        student=create_student(),
        competition=create_student_has_competition_log(),
        score=100
        )
        return studentHasCompetition_obj

def create_question():
    if Question.objects.filter(id=1).exists():
        return  Question.objects.get(id=1)
    else:
        question_obj = Question.objects.create(
        id=1,
        word=create_word(),
        question_type='中译英',
        question='你好',
        question_difficulty='easy',
        correct_option='hello',
        disturbance_option1='book',
        disturbance_option2='eat',
        disturbance_option3='food'
        )
        return question_obj

def create_pk_log():
    if PKLog.objects.filter(id=1).exists():
        return PKLog.objects.get(id=1)
    else:
        pk_log_obj = PKLog.objects.create(
        id=1,
        competition=create_competitionInfo(),
        student=create_student(),
        question=create_question(),
        time=5,
        answer='hello',
        is_right=True
        )
        return pk_log_obj

def create_infinite_challenge_log():
    if InfiniteChallengeLog.objects.filter(id=1).exists():
        return InfiniteChallengeLog.objects.get(id=1)
    else:
        InfiniteChallengeLog_obj = InfiniteChallengeLog.objects.create(
        id=1,
        student=create_student(),
        competition=create_competitionInfo(),
        question=create_question(),
        is_right=True
        )
        return InfiniteChallengeLog_obj
