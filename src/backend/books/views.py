'''
@file books应用的views.py文件
'''
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from study.models import WordLog, Question
from .models import *
import json
import random

def get_word(request):
    '''
    获取一个学生未学过单词的word，sentence属性
    调用方式GET
    @author 陶磊
    @brief 通过获取的学生id筛选出对应的word_log里的集合，从这个集合中取出word_id的值，以及其word_id对应在ExampleSentence表中所有属性的值
    @param students_id 学生id
    @return 字典数组 tmp_obj,每个元素的两个属性分别为sentence和data
    @return get word failed 调用方式为POST
    '''
    send_data = []
    if request.method == 'GET':
        student_id = request.GET.get('student_id', None)
        category_id = request.GET.get('category', None)
        word_log = WordLog.objects.filter(student_id=student_id, \
            category_id=category_id, status=-1)
        search_result = json.loads(serializers.serialize('json', word_log, ensure_ascii=False))[0:7]
        for one_word in search_result:
            tmp_obj = {}
            word_id = one_word['fields']['word']
            word = Word.objects.filter(id=word_id)
            result = json.loads(serializers.serialize('json', word, ensure_ascii=False))
            sentence = ExampleSentence.objects.filter(id=word_id)
            sentence_data = json.loads(serializers.serialize('json', sentence, ensure_ascii=False))
            tmp_obj['sentence'] = sentence_data
            tmp_obj['data'] = result
            send_data.append(tmp_obj)
        return HttpResponse(json.dumps(send_data))
    return HttpResponse('get word failed')

def generate_question(request):
    '''
    生成题目
    调用方式GET
    @author 陶磊
    @brief 对于word表中的每个单词，生成中译英，英译中两种题目，每隔题目随机生成三个干扰选项及一个正确选项将结果插入question_en，question_ech表中
    @return generate_question success 生成题目成功
    @return generate_question failed 生成题目失败
    '''
    if request.method == 'GET':
        words = Word.objects.all()
        length = len(words)
        tmp_arr = []
        for i in range(0, length):
            tmp_arr.append(i)
        for i in range(0, length):
            word = words[i]
            random_arr = tmp_arr.copy()
            random_arr.pop(i)
            random.shuffle(random_arr)
            question_en = Question(
                question_type='中选英',
                question=word.explains,
                question_difficulty=word.difficult,
                correct_option=word.word,
                disturbance_option1=words[random_arr[0]].word,
                disturbance_option2=words[random_arr[1]].word,
                disturbance_option3=words[random_arr[2]].word,
                word_id=word.id
            )
            question_en.save()
            question_ch = Question(
                question_type='英选中',
                question=word.word,
                question_difficulty=word.difficult,
                correct_option=word.explains,
                disturbance_option1=words[random_arr[0]].explains,
                disturbance_option2=words[random_arr[1]].explains,
                disturbance_option3=words[random_arr[2]].explains,
                word_id=word.id
            )
            question_ch.save()
        return HttpResponse('generate_question success')
    return HttpResponse('generate_question failed')

def generate_unit_word(request):
    '''
    生成单元单词关联表
    调用方式GET
    @author 陶磊
    @brief 遍历Word表
    @return generate_unit_word success 成功生成
    @return generate_unit_word failed 失败生成
    '''
    if request.method == 'GET':
        words = Word.objects.all()
        for word in words:
            word_id = word.id
            classify = Classification.objects.filter(word=word_id)
            category = json.loads(serializers.serialize('json', \
                classify, ensure_ascii=False))[0]['fields']['category']
            sequence = json.loads(serializers.serialize('json', \
                classify, ensure_ascii=False))[0]['fields']['sequence']
            unit = 0
            if sequence % 14 != 0:
                unit = sequence // 14 + 1
            else:
                unit = sequence // 14
            unit_set = UnitInfo.objects.get(unit_num=unit, book_id=category)
            if unit_set:
                unit_word = UnitWord(
                    word=word,
                    unit=unit_set
                )
                unit_word.save()
        return HttpResponse('generate_unit_word success')
    return HttpResponse('generate_unit_word failed')

def get_courses(request):
    '''
    获取所有课程信息
    调用方式GET
    @author 陶磊
    @brief 遍历Category表，返回字典数组
    @return course字典数组 获取课程成功
    @return GetFail 获取所有课程信息失败
    '''
    if request.method == 'GET':
        courses = Category.objects.all()
        courses = serializers.serialize('json', courses, ensure_ascii=False)
        courses = json.loads(courses)
        courses = json.dumps(courses)
        return HttpResponse(courses)
    return HttpResponse('GetFail')

def get_book_name(request):
    '''
    获取教材名称
    调用方式GET
    @author 陶磊
    @brief 获取book_id,从Category里找到其对应书名返回
    @param book_id
    @return book_name 对应的书的名字
    @return get_word_name failed 获取教材名称失败
    '''
    if request.method == 'GET':
        book = Category.objects.filter(
            id=request.GET.get('books_id')
        )
        book_name = json.loads(
            serializers.serialize('json', book, fields=('category'), ensure_ascii=False)
        )
        return HttpResponse(json.dumps(book_name))
    return HttpResponse('get_word_name failed')

def get_course_info(request):
    '''
    获取课程信息
    调用方式GET
    @author 陶磊
    @brief 获取所有课程的所有信息
    @return course_info 返回所有课程信息
    @return get_course_info failed 获取课程信息失败
    '''
    if request.method == 'GET':
        course_info = Category.objects.all()
        course_info = serializers.serialize('json', course_info, ensure_ascii=False)
        course_info = json.loads(course_info)
        return JsonResponse(course_info, safe=False)
    return HttpResponse('get_course_info failed')
