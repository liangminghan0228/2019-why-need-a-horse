'''
study应用路由处理函数模块
'''
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from books.models import Word, Category, Classification, UnitWord
from information.models import Student
import json
import datetime
from .models import *
from django.core import serializers
import random
import time
from django.db.models import Count

def teacher_test_record(request):
    '''
    教师端获取测试记录
    调用方式 POST
    @author 梁明晗
    @param student_id 学生id
    @return res 成功返回学生测试记录
    @return teacher_test_record failed 获取失败
    '''
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        test_log = TestLog.objects.filter(student=student_id)
        res = []
        for log in test_log:
            item = Category.objects.filter(id=log.book.id)
            book_name = item[0].category
            item = {'book_name': book_name, 'test_type': log.test_type,\
                'is_pass': log.is_pass, 'test_score': log.test_score,\
                'test_time': log.test_time.strftime('%Y-%m-%d %H:%M:%S')}
            res.append((item))
        return HttpResponse(json.dumps(res), content_type="application/json")
    return JsonResponse('teacher_test_record failed')


def subscribe_course():
    '''
    暂无
    '''


def get_study_statistic(request):
    '''
    教师端获取班级学生最近七天学习记录
    调用方式 GET
    @author 陶磊
    @param class 班级
    @return result 成功返回班级学习记录
    @return get seven days statistic data failed 获取失败
    '''
    if request.method == 'GET':
        class_value = request.GET.get('class')
        result = {
            'student': [],
            'train': [],
            'vocabulary': [],
            'time': [],
            'and': []
        }
        student_set = Student.objects.filter(classes=class_value)
        student = json.loads(serializers.serialize(
            'json', student_set, ensure_ascii=False))
        for item in student:
            result['student'].append(item['fields']['student_name'])
            word_num = len(WordLog.objects.filter(student=item['pk']))
            result['train'].append(word_num)
            vocabulary = len(WordLog.objects.filter(student=item['pk'], status__gt=0))
            result['vocabulary'].append(vocabulary)
            result['and'].append(word_num + vocabulary)
            study_time_set = StudyLog.objects.filter(student=item['pk'])
            time_total = 0
            for study_time in study_time_set:
                time_total += study_time.study_duration
            result['time'].append(time_total)
        return HttpResponse(json.dumps(result))
    return HttpResponse('get seven days statistic data failed')

def get_study_statistic_seven(request):
    '''
    教师端获取班级学生最近七天学习记录
    调用方式 GET
    @author 陶磊
    @param class 班级
    @return result 成功返回班级学习记录
    @return get seven days statistic data failed 获取失败
    '''
    if request.method == 'GET':
        class_value = request.GET.get('class')
        today = datetime.date.today()
        delta_day = today - datetime.timedelta(days=7)
        result = {
            'student': [],
            'train': [],
            'vocabulary': [],
            'time': [],
            'and': []
        }
        student_set = Student.objects.filter(classes=class_value)
        student = json.loads(serializers.serialize(
            'json', student_set, ensure_ascii=False))
        for item in student:
            result['student'].append(item['fields']['student_name'])
            word_num = len(WordLog.objects.filter(student=item['pk'], \
                study_date__lte=today, study_date__gte=delta_day))
            result['train'].append(word_num)
            vocabulary = len(WordLog.objects.filter(student=item['pk'], \
                status__gt=0, study_date__lte=today, study_date__gte=delta_day))
            result['vocabulary'].append(vocabulary)
            result['and'].append(word_num + vocabulary)
            study_time_set = StudyLog.objects.filter(student=\
                item['pk'], study_date__lte=today, study_date__gte=delta_day)
            time_total = 0
            for study_time in study_time_set:
                time_total += study_time.study_duration
            result['time'].append(time_total)
        return HttpResponse(json.dumps(result))
    return HttpResponse('get seven days statistic data failed')


def get_study_date(request):
    '''
    学生端获取学生学习日期
    调用方式 POST
    @author 梁明晗
    @param studentID 学生id
    @return result 成功返回学生学习日期
    '''
    student_id = request.POST.get('studentID')
    study_date = StudyLog.objects.filter(student=student_id)
    study_date = serializers.serialize('json', study_date, ensure_ascii=False)
    study_date = json.loads(study_date)
    return JsonResponse(study_date, safe=False)


def card_today(request):
    '''
    教师端获取班级学生最近七天学习记录
    调用方式 POST
    @author 梁明晗
    @param studentID 学生id
    @param today 今日学习日期
    @return 打卡成功 返回打卡成功
    '''
    student_id = request.POST.get('studentID')
    today = request.POST.get('today')
    a_study_log = StudyLog(student_id=student_id, study_date=today)
    a_study_log.save()
    coin_total = Student.objects.filter(id=\
        student_id).values('coin_total')[0]['coin_total'] + 10
    Student.objects. \
        filter(id=student_id).\
        update(coin_total=coin_total)
    return HttpResponse('打卡成功')


def get_learned_word(request):
    '''
    暂无
    '''
    if request.method == 'GET':
        pass

    return HttpResponse('response data')


def add_competition(request):
    '''
    暂无
    '''
    if request.method == 'POST':
        pass
    return HttpResponse('response data')


def get_statistic_with_student_id(request):
    '''
    根据学生id获取其相关学习记录
    调用方式 GET
    @author 陶磊
    @param studentID 学生id
    @return result 成功返回相关记录
    @return get statistic data failed 获取失败
    '''
    if request.method == 'GET':
        result = []
        student_id = request.GET.get('student_id')
        study_log = TestLog.objects.filter(student_id=student_id)
        study_log_obj = json.loads(serializers.serialize(
            'json', study_log, ensure_ascii=False))
        for study_log_item in study_log_obj:
            item = {}
            book = Category.objects.filter(
                id=study_log_item['fields']['book']
            )
            item['book'] = json.loads(
                serializers.serialize('json', book, ensure_ascii=False)
            )[0]['fields']['category']
            item['data'] = study_log_item['fields']
            result.append(item)
        return HttpResponse(json.dumps(result))
    return HttpResponse('get statistic data failed')

def get_bar_statistic(request):
    '''
    根据学生id获取柱状图相关学习记录
    调用方式 GET
    @author 陶磊
    @param studentID 学生id
    @return result 成功返回相关记录
    @return get statistic data failed 获取失败
    '''
    if request.method == 'GET':
        result = []
        student_id = request.GET.get('student_id')
        today = datetime.date.today()
        for i in range(0, 7):
            delta_day = today - datetime.timedelta(days=i)
            all_word = WordLog.objects.filter(
                student_id=student_id, study_date=delta_day)
            word_count = len(json.loads(serializers.serialize(
                'json', all_word, ensure_ascii=False)))
            result.append(word_count)
        return HttpResponse(json.dumps(result))
    return HttpResponse('get statistic data failed')


def get_word_book(request):
    '''
    暂无
    '''
    if request.method == 'GET':
        pass
    return HttpResponse('response data')


def get_word(request):
    '''
    获取单词
    调用方式 GET
    @author 孙晓冰
    @param group 分组
    @param oneGroupCount 一组数量
    @param order 顺序
    @return result 成功返回相关单词
    @return get_word failed 获取失败
    '''
    result = []
    if request.method == 'GET':
        group = int(request.GET.get('group'))
        one_group_count = int(request.GET.get('oneGroupCount'))
        order = request.GET.get('order')
        if order == 'familar':
            word_data = WordLog.objects.filter(
                student=request.GET.get('student_id'),
                category=request.GET.get('category_id')
            ).order_by('status')
        else:
            word_data = WordLog.objects.filter(
                student=request.GET.get('student_id'),
                category=request.GET.get('category_id')
            ).order_by('word__word')
        group_len = word_data.count()
        if (group - 1) * one_group_count >= group_len:
            return HttpResponse('none')
        else:
            start = (group - 1) * one_group_count
            end = group * one_group_count
            if group * one_group_count > group_len:
                end = group_len
            word_data = word_data[start: end]
        word_set = json.loads(serializers.serialize(
            'json', word_data, ensure_ascii=False))
        for one_word in word_set:
            item = {}
            a_word = Word.objects.filter(
                id=one_word['fields']['word']
            )
            item['spelling'] = json.loads(
                serializers.serialize('json', a_word, ensure_ascii=False)
            )[0]['fields']['word']
            item['status'] = one_word['fields']['status']
            result.append(item)
        return HttpResponse(json.dumps(result))
    return HttpResponse('get_word failed')


def register_course(request):
    '''
    教师端给学生注册课程
    调用方式 POST
    @author 张彭豪
    @param student_id 学生id
    @return SuccessRegister 注册成功
    @return FailRegister 注册失败
    '''
    if request.method == 'POST':
        param = json.loads(request.body.decode())
        books = []
        student_id = param[0]['student_id']
        i = 0
        while i < len(param[1]):
            books.append(param[1][i])
            i = i + 1
        i = 0
        while i < len(books):
            book_id = books[i]
            bookset = StudentBook.objects.filter(
                book=book_id, student=student_id)
            if bookset.exists():
                i = i + 1
                continue
            judge = StudentBook.objects.filter(student=student_id)
            status = True
            if judge.exists():
                status = False
            student_book_set = StudentBook.objects.create(
                book_id=book_id, student_id=student_id, status=status)
            student_book_set.save()
            unit_set = UnitInfo.objects.filter(
                book_id=book_id).values('unit_id', 'unit_num')
            k = 0
            while k < unit_set.count():
                student_unit_set = StudentUnit.objects.create(
                    status='beforelearning',
                    category_id=book_id,
                    student_id=student_id,
                    unit_id=unit_set[k]['unit_id'],
                    unit_num=unit_set[k]['unit_num'])
                student_unit_set.save()
                k = k + 1
            wordset = Classification.objects.filter(
                category=book_id).values('word')
            j = 0
            while j < wordset.count():
                unit_id_set = UnitWord.objects.filter(
                    word_id=wordset[j]['word']).values('unit_id')
                if unit_id_set.count() == 0:
                    j = j + 1
                    continue
                unit_id = unit_id_set[0]['unit_id']
                unit_num_set = UnitInfo.objects.filter(
                    unit_id=unit_id).values('unit_num')
                if unit_num_set.count() == 0:
                    j = j + 1
                    continue
                unit_num = unit_num_set[0]['unit_num']
                word_log = WordLog.objects.create(
                    word_id=wordset[j]['word'],
                    student_id=student_id,
                    category_id=book_id,
                    unit_id=unit_id,
                    unit_num=unit_num,
                    status=-1,
                    rank=0,
                    study_date='1900-1-1'
                )
                word_log.save()
                j = j + 1
            i = i + 1
        return HttpResponse('SuccessRegister')
    return HttpResponse('FailRegister')


def show_register_result(request):
    '''
    根据学生id获取学生注册课程相关记录
    调用方式 GET
    @author 张彭豪
    @param student_id 学生id
    @return param 所注册课程记录
    @return FailMessage 获取失败
    '''
    if request.method == 'GET':
        student_id = request.GET.get('student_id')
        student_set = StudentBook.objects.filter(student=student_id).order_by('-id')
        i = 0
        param = []
        while i < student_set.count():
            tmp = {
                'id': student_set[i].book.id,
                'name': student_set[i].book.category,
                'status': student_set[i].status
            }
            param.append(tmp)
            i = i + 1
        param = json.dumps(param)
        return HttpResponse(param)
    return HttpResponse('FailMessage')


def get_unit_info(request):
    '''
    暂无
    '''
    if request.method == 'GET':
        pass
    return HttpResponse('response data')


def get_questions_of_test_to_end(request):
    '''
    暂无
    '''
    if request.method == 'POST':
        pass
    return HttpResponse('response message')


def get_words_of_test_to_end(request):
    '''
    暂无
    '''
    if request.method == 'POST':
        pass
    return HttpResponse('response message')


def student_test_record(request):
    '''
    暂无
    '''
    if request.method == 'GET':
        pass
    return HttpResponse('response data')


def calendar(request):
    '''
    暂无
    '''
    if request.method == 'GET':
        pass
    return HttpResponse('response data')

def leader_board(request):
    '''
    获取排行榜相关记录
    调用方式 POST
    @author 梁明晗
    @param student_id 学生id
    @return rank 排行榜排名结果
    @return leader_board_failed 获取失败
    '''
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        today = time.strftime('%Y-%m-%d', time.localtime())
        today_record = StudyLog.objects.filter(
            study_date=today, student=student_id)
        res = []
        if today_record.exists():
            coin_number = today_record.values('coin_number')[0]['coin_number']
            res.append(coin_number)
            coin_rank = StudyLog.objects.filter(
                coin_number__gt=coin_number).count() + 1
            res.append(coin_rank)
            today_duration = today_record.values('study_duration')[
                0]['study_duration']
            res.append(today_duration)
            today_rank = StudyLog.objects.filter(
                study_duration__gt=today_duration).count() + 1
            res.append(today_rank)
        all_record = Student.objects.filter(id=student_id)
        if all_record.exists():
            all_duration = all_record.values('cumulative_study_duration')[
                0]['cumulative_study_duration']
            res.append(all_duration)
            all_rank = Student.objects.filter(
                cumulative_study_duration__gt=all_duration).count() + 1
            res.append(all_rank)
        rank = {'coin_number': res[0], 'coin_rank': res[1], 'today_duration': res[2],
                'today_rank': res[3], 'all_duration': res[4], 'all_rank': res[5]}
        return HttpResponse(json.dumps(rank), content_type="application/json")
    return HttpResponse('leader_board_failed')

def leader_coin_board(request):
    '''
    获取排行榜金币榜相关记录
    调用方式 GET
    @author 梁明晗
    @return res 金币排行榜排名结果
    @return leader_coin_board failed 获取失败
    '''
    if request.method == 'GET':
        order = StudyLog.objects.filter(study_date=time.strftime(
            '%Y-%m-%d', time.localtime())).order_by('-coin_number')
        res = []
        for coin in order:
            item = Student.objects.filter(id=coin.student.id)
            avatar = item[0].avatar
            name = item[0].student_name
            item = {'id': coin.student.id, 'name': name, 'coin_number': coin.coin_number,
                    'study_duration': coin.study_duration, 'avatar': avatar}
            res.append(item)
        return HttpResponse(json.dumps(res), content_type="application/json")
    return HttpResponse('leader_coin_board failed')


def leader_today_board(request):
    '''
    获取今日排行榜相关记录
    调用方式 GET
    @author 梁明晗
    @return res 今日排行榜结果
    @return leader_today_board failed 获取失败
    '''
    if request.method == 'GET':
        order = StudyLog.objects.filter(study_date=time.strftime(
            '%Y-%m-%d', time.localtime())).order_by('-study_duration')
        res = []
        for coin in order:
            item = Student.objects.filter(id=coin.student.id)
            avatar = item[0].avatar
            name = item[0].student_name
            item = {'id': coin.student.id, 'name': name, 'coin_number': coin.coin_number,
                    'study_duration': coin.study_duration, 'avatar': avatar}
            res.append(item)
        return HttpResponse(json.dumps(res), content_type="application/json")
    return HttpResponse('leader_today_board failed')


def leader_all_board(request):
    '''
    获取所有排行榜相关记录
    调用方式 GET
    @author 陶磊
    @return order 所有排行榜结果
    @return leader_all_board failed 获取失败
    '''
    if request.method == 'GET':
        order = Student.objects.all().order_by('-cumulative_study_duration')
        order = serializers.serialize('json', order, ensure_ascii=False)
        order = json.loads(order)
        return JsonResponse(order, safe=False)
    return HttpResponse('leader_all_board failed')


def get_unit_list(request):
    '''
    获取单元列表相关记录
    调用方式 GET
    @author 孙晓冰
    @param category_id 单元id
    @param student_id 学生id
    @return unit_list 单元列表
    @return get_unit_list failed 获取失败
    '''
    if request.method == 'GET':
        unit = StudentUnit.objects.filter(
            category=request.GET.get('category_id'),
            student=request.GET.get('student_id')
        )
        unit_list = json.loads(
            serializers.serialize('json', unit, ensure_ascii=False))
        return HttpResponse(json.dumps(unit_list))
    return HttpResponse('get_unit_list failed')

def update_unit_status(request):
    '''
    更新单元状态
    调用方式 GET
    @author 陶磊
    @param category_id 单元id
    @param student_id 学生id
    @return update_unit_status success 更新单元状态成功
    @return update_unit_status failed 更新单元状态成功失败
    '''
    if request.method == 'GET':
        words_set = WordLog.objects.filter(
            category=request.GET.get('category_id'),
            student=request.GET.get('student_id'),
            status__gte=0
        ).values('unit_id').annotate(total_num=Count('unit_num'))
        for item in words_set:
            num = item['total_num']
            unit_info_set = UnitInfo.objects.filter(unit_id=item['unit_id'])
            unit_info = json.loads(serializers.serialize('json', unit_info_set, ensure_ascii=False))
            is_equal = (unit_info[0]['fields']['total_number'] == num)
            if is_equal:
                StudentUnit.objects.filter(unit=item['unit_id']).update(status='complete')
        return HttpResponse('update_unit_status success')
    return HttpResponse('update_unit_status failed')

def get_opened_course(request):
    '''
    获取已开通课程
    调用方式 POST
    @author 梁明晗
    @param student_id 学生id
    @return opened_course_info 返回已开通课程
    @return get_opened_course_failed 获取失败
    '''
    if request.method == 'GET':
        student_id = request.GET.get('student_id')
        opened_course_info = StudentBook.objects.filter(student=student_id)
        opened_course_info = serializers.serialize('json', opened_course_info, ensure_ascii=False)
        opened_course_info = json.loads(opened_course_info)
        return JsonResponse(opened_course_info, safe=False)
    return HttpResponse('get_opened_course_failed')


def get_current_course(request):
    '''
    根据学生id获取当前已开通课程
    调用方式 GET
    @author 梁明晗
    @param student_id 学生id
    @return res 返回已开通课程
    @return get_current_course_failed 获取失败
    '''
    if request.method == 'GET':
        student_id = request.GET.get('student_id')
        current_course_info = StudentBook.objects.filter(student=student_id, status=True)
        if current_course_info.exists():
            book_id = current_course_info.values('book')[0]['book']
            res = []
            for course in Category.objects.all():
                if course.id == book_id:
                    res.append({'book_id': book_id, 'book_name': course.category})
            return HttpResponse(json.dumps(res[0]))
    return HttpResponse('get_current_course_failed')

def change_course(request):
    '''
    根据学生id切换课程开通状态
    调用方式 POST
    @author 梁明晗
    @param student_id 学生id
    @param book_id 课程id
    @return opened_course_info 已开通课程信息
    '''
    student_id = request.POST.get('student_id', None)
    book_id = request.POST.get('book_id', None)
    StudentBook.objects.filter(student=student_id).update(status=False)
    StudentBook.objects.filter(
        student=student_id, book=book_id).update(status=True)
    opened_course_info = StudentBook.objects.filter(student=student_id)
    opened_course_info = serializers.serialize(
        'json', opened_course_info, ensure_ascii=False)
    opened_course_info = json.loads(opened_course_info)
    return JsonResponse(opened_course_info, safe=False)


def get_pretest_word(request):
    '''
    根据学生id和课程id获取学前测试单词
    调用方式 GET
    @author 孙晓冰
    @param student_id 学生id
    @param category_id 课程id
    @return result 学前测试单词
    @return get_pretest_word failed 获取失败
    '''
    result = []
    if request.method == 'GET':
        word = WordLog.objects.filter(
            student=request.GET.get('student_id'),
            category=request.GET.get('category_id')
        ).order_by('word__difficult', 'word__junior_level', 'word__senior_level')
        word_set = json.loads(serializers.serialize(
            'json', word, ensure_ascii=False))
        for one_word in word_set:
            item = {}
            question = Question.objects.filter(
                word=one_word['fields']['word']
            )
            item['question'] = json.loads(
                serializers.serialize('json', question, ensure_ascii=False)
            )[0]['fields']
            item['id'] = json.loads(
                serializers.serialize('json', question, ensure_ascii=False)
            )[0]['pk']
            result.append(item)
        return HttpResponse(json.dumps(result))
    return HttpResponse('get_pretest_word failed')


def set_word_rank(request):
    '''
    根据学生id和单词id设置单词复习时出现顺序
    调用方式 GET
    @author 陶磊
    @param student_id 学生id
    @param word_id 单词id
    @param word_level 单词复习出现次序
    @return set word rank success 设置成功
    '''
    word_id = request.GET.get('word_id')
    word_level = request.GET.get('word_level')
    student_id = request.GET.get('student_id')
    WordLog.objects.filter(student_id=student_id, \
        word_id=word_id).update(rank=word_level, study_date=datetime.date.today())
    return HttpResponse('set word rank success')

def set_word_status(request):
    '''
    根据学生id和单词id设置单词状态
    调用方式 GET
    @author 陶磊
    @param student_id 学生id
    @param word_id 单词id
    @param word_status 单词状态
    @return set word rank success 设置成功
    '''
    word_id = request.GET.get('word_id')
    word_status = request.GET.get('word_status')
    student_id = request.GET.get('student_id')
    WordLog.objects.filter(student_id=student_id, \
        word_id=word_id).update(status=word_status, study_date=datetime.date.today())
    return HttpResponse('set word rank success')

def add_pretest_log(request):
    '''
    添加学前测试记录
    调用方式 POST
    @author 孙晓冰
    @param student_id 学生id
    @param question_set 问题集
    @param book_id 课程id
    @return add_pretest_log success 添加成功
    @return add_pretest_log failed 添加失败
    '''
    if request.method == 'POST':
        question_data = json.loads(request.body.decode())
        question_id = question_data['question_set']
        student_id = question_data['student_id']
        book_id = question_data['book_id']
        for item in question_id:
            question = PretestLog.objects.create(
                question_id=item,
                student_id=student_id,
                book_id=book_id
            )
            question.save()
        return HttpResponse('add_pretest_log success')
    return HttpResponse('add_pretest_log failed')


def add_test_log(request):
    '''
    添加测试记录
    调用方式 GET
    @author 孙晓冰
    @param student_id 学生id
    @param test_typeon_set 测试类型
    @param book_id 课程id
    @param score 测试得分
    @return add_test_log success 添加成功
    @return add_test_log failed 添加失败
    '''
    if request.method == 'GET':
        student_id = request.GET.get('student_id')
        book_id = request.GET.get('book_id')
        test_type = request.GET.get('test_type')
        test_time = datetime.datetime.now()
        test_score = request.GET.get('score')
        is_pass = False
        test_score = int(test_score)
        if test_score >= 60:
            is_pass = True
        test_log = TestLog.objects.create(
            student_id=student_id,
            book_id=book_id,
            test_type=test_type,
            test_time=test_time,
            test_score=test_score,
            is_pass=is_pass
        )
        test_log.save()
        return HttpResponse('add_test_log success')
    return HttpResponse('add_test_log failed')


def get_after_test(request):
    '''
    获取学后测试题目
    调用方式 GET
    @author 孙晓冰
    @param student_id 学生id
    @param book_id 课程id
    @return result 学后测试题目
    @return get_after_test failed 获取失败
    '''
    if request.method == 'GET':
        result = []
        book_id = request.GET.get('book_id')
        student_id = request.GET.get('student_id')
        question_set = PretestLog.objects.filter(
            student=student_id,
            book=book_id
        )
        question_set = json.loads(serializers.serialize(
            'json', question_set, ensure_ascii=False))
        for item in question_set:
            a_question = Question.objects.filter(id=item['fields']['question'])
            a_question = json.loads(serializers.serialize(
                'json', a_question, ensure_ascii=False))
            result.append(a_question[0])
        return HttpResponse(json.dumps(result))
    return HttpResponse('get_after_test failed')


def get_book_test(request):
    '''
    获取课程一测到底测试题目
    调用方式 GET
    @author 孙晓冰
    @param student_id 学生id
    @param group 分组信息
    @param oneGroupCount 一组数量
    @return result 课程一测到底测试题目
    @return get_book_word failed 获取失败
    '''
    if request.method == 'GET':
        result = []
        book_id = request.GET.get('book_id')
        group = int(request.GET.get('group'))
        one_group_count = int(request.GET.get('oneGroupCount'))
        word_set = Classification.objects.filter(category=book_id)
        group_len = word_set.count()
        if (group-1) * one_group_count >= group_len:
            return HttpResponse('none')
        else:
            start = (group - 1) * one_group_count
            end = group * one_group_count
            if group * one_group_count > group_len:
                end = group_len
            word_set = word_set[start:end]
        word_set = json.loads(serializers.serialize(
            'json', word_set, ensure_ascii=False))
        for a_word in word_set:
            index = random.randint(0, 1)
            a_question = Question.objects.filter(word=a_word['fields']['word'])
            a_question = json.loads(serializers.serialize(
                'json', a_question, ensure_ascii=False))
            result.append(a_question[index])
        return HttpResponse(json.dumps(result))
    return HttpResponse('get_book_word failed')


def get_review_test(request):
    '''
    获取巩固测试题目
    调用方式 GET
    @author 孙晓冰
    @param student_id 学生id
    @param book_id 课程id
    @return result 课程巩固测试题目
    @return get_review_word failed 获取失败
    '''
    if request.method == 'GET':
        result = []
        book_id = request.GET.get('book_id')
        student_id = request.GET.get('student_id')
        test_date = datetime.date.today()
        word_set = WordLog.objects.filter(
            student=student_id,
            category=book_id,
            study_date=test_date
        )
        word_set = word_set.exclude(
            status=-1
        )
        word_set = json.loads(serializers.serialize(
            'json', word_set, ensure_ascii=False))
        length = len(word_set)
        if length >= 10:
            number = random.sample(range(0, length), 10)
        else:
            number = random.sample(range(0, length), length)
        for i in number:
            index = random.randint(0, 1)
            a_question = Question.objects.filter(
                word=word_set[i]['fields']['word'])
            question = json.loads(serializers.serialize(
                'json', a_question, ensure_ascii=False))
            result.append(question[index])
        return HttpResponse(json.dumps(result))
    return HttpResponse('get_review_word failed')

def get_test_score(request):
    '''
    获取测试得分记录
    调用方式 GET
    @author 孙晓冰
    @param student_id 学生id
    @param book_id 课程id
    @param test_type 测试类型
    @return test_score 测试得分
    @return get_pretest_score failed 获取失败
    '''
    if request.method == 'GET':
        student_id = request.GET.get('student_id')
        book_id = request.GET.get('book_id')
        test_type = request.GET.get('test_type')
        test = TestLog.objects.filter(
            student=student_id,
            book=book_id,
            test_type=test_type
        )
        if test.count() == 0:
            return HttpResponse('none')
        index = test.count() - 1
        test = json.loads(serializers.serialize('json', test, ensure_ascii=False))
        a_test = test[index]
        test_score = a_test['fields']['test_score']
        return HttpResponse(json.dumps(test_score))
    return HttpResponse('get_pretest_score failed')
