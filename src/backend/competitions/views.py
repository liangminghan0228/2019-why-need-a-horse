from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from study.models import *
from books.models import *
import json
from django.core import serializers
import time
import random

def generate_ghost():
    if Student.objects.filter(id='Ghost').count() == 0:
        ghost = Student.objects.create(
            id='Ghost',
            student_name='Ghost',
            email='GHOST@GHOST.com',
            login_times=0,
            coin_total=0,
            register_time=time.strftime('%Y-%m-%d', time.localtime()),
            pay_status=False,
            vocabularies=0,
            cumulative_study_duration=0,
            grade=1,
            school='GHOSTSCHOOL',
            last_login=time.strftime(
                '%Y-%m-%d %H:%M:%S', time.localtime()),
            classes_id=1
        )
        ghost.save()
        return True
    return None

def generate_pk_ghost_log(competition_id, student_id, question_num):
    '''
    产生幽灵对战记录
    @author 张彭豪
    @brief 向PKLog和StudentHasCompetitionLog两个表插入随机生成的信息
    @param competition_id 比赛id
    @param student_id 学生id
    @param question_num 问题数目
    @return SuccessInsert 成功创建一个幽灵对战实例
    '''
    deviation = 15
    generate_ghost()
    book_id = CompetitionInfo.objects.filter(id=competition_id)[0].book_id
    word_set = []
    if book_id != 0:
        word_set.append(Classification.objects.filter(category=book_id).values('word_id'))
    else:
        word_set.append(Classification.objects.all().values('word_id'))
    k = 0
    word_set = word_set[0]
    flag = 0
    while flag < question_num:
        if k == word_set.count() - 1:
            k = 0
        word_id = word_set[k]['word_id']
        index = random.randint(0, 1)
        question = Question.objects.filter(word_id=word_id)
        if question.count() > 1:
            question = question[index]
        else:
            question = question[0]
        rand = random.randint(0, 3)
        is_right = False
        if rand == 0:
            answer = question.disturbance_option1
        elif rand == 1:
            answer = question.disturbance_option2
        elif rand == 2:
            answer = question.disturbance_option3
        else:
            answer = question.correct_option
            is_right = True
        avg = random.randint(40, 60)
        rand_time = random.randint(avg - deviation, avg + deviation) * 100
        pklogInstance = PKLog.objects.create(
            competition_id=competition_id,
            student_id=student_id,
            question_id=question.id,
            is_right=is_right,
            time=rand_time,
            answer=answer
        )
        pklogInstance.save()
        k = k + 1
        flag = flag + 1
    log = StudentHasCompetitionLog.objects.create(
        student_id=student_id,
        competition_id=competition_id,
        score=0
    )
    log.save()
    return HttpResponse('SuccessInsert')

def get_pk_data(request):
    '''
    获得PKLog的数据
    调用方式POST
    @author 张彭豪
    @brief 随机生成PK比赛队手的id，获取其头像，生成其比赛信息
    @param competition_id 比赛id
    @return 返回幽灵的id，头像，及其对应的PK_data
    @return FailResponse 获取比赛信息失败
    '''
    if request.method == 'POST':
        question_num = 30
        param = json.loads(request.body.decode())
        competition_id = param[1]
        if competition_id == 0:
            return HttpResponse('FailResponse')
        pk_data = []
        judge = StudentHasCompetitionLog.objects.filter(competition_id=competition_id)
        other_id = ''
        if judge.count() == 0:
            generate_pk_ghost_log(competition_id, 'Ghost', question_num)
            other_id = 'Ghost'
        else:
            other_list = []
            for item in judge:
                pk_log_set = PKLog.objects.filter(competition_id=\
                    competition_id, student_id=item.student.id)
                if pk_log_set.count() < question_num:
                    continue
                else:
                    other_list.append(item.student.id)
            if other_list:
                other_id = other_list[random.randint(0, len(other_list) - 1)]
            else:
                generate_pk_ghost_log(competition_id, 'Ghost', question_num)
                other_id = 'Ghost'
        pk_log_set = PKLog.objects.filter(competition_id=\
            competition_id, student_id=other_id)
        i = 0
        tmp = {}
        while i < question_num:
            tmp['other_choose'] = pk_log_set[i].answer
            tmp['is_right'] = pk_log_set[i].is_right
            tmp['time'] = pk_log_set[i].time
            tmp['question_id'] = pk_log_set[i].question.id
            tmp['word_id'] = pk_log_set[i].question.word_id
            tmp['question_type'] = pk_log_set[i].question.question_type
            tmp['question'] = pk_log_set[i].question.question
            tmp['correct_option'] = pk_log_set[i].question.correct_option
            tmp['disturbance_option1'] = pk_log_set[i].question.disturbance_option1
            tmp['disturbance_option2'] = pk_log_set[i].question.disturbance_option2
            tmp['disturbance_option3'] = pk_log_set[i].question.disturbance_option3
            pk_data.append(tmp)
            tmp = {}
            i = i + 1
        other = serializers.serialize('json', Student.objects.filter(id=other_id), \
            fields=('id', 'student_name', 'avatar'), ensure_ascii=False)
        other = json.loads(other)
        result = {'other': other, 'pk_data': pk_data}
        result = json.dumps(result)
        return HttpResponse(result)
    return HttpResponse('FailResponse')

def add_pk_log(request):
    '''
    添加PKLog记录
    调用方式POST
    @author 张彭豪
    @brief 向StudentHasCompetitionLog表中插入比赛记录信息
    @param pk_log_set
    @param student_id 学生id
    @param competition_id 比赛id
    @score 分数
    @return SuccessInsert 添加比赛信息成功
    @return FailResponse 添加比赛信息失败
    '''
    if request.method == 'POST':
        param = json.loads(request.body.decode())
        pk_log_set = param[0]
        student_id = param[1]
        competition_id = param[2]
        score = param[3]
        for item in pk_log_set:
            pklog_instance = PKLog.objects.create(
                answer=item['answer'],
                competition_id=item['competitionId'],
                is_right=item['isRight'],
                question_id=item['questionId'],
                student_id=item['studentId'],
                time=item['time']
            )
            pklog_instance.save()
        judge = StudentHasCompetitionLog.objects.filter(competition_id=competition_id, student_id=student_id)
        if judge.exists():
            judge.update(score=score)
        else:
            log = StudentHasCompetitionLog.objects.create(
                student_id=student_id,
                competition_id=competition_id,
                score=score
            )
            log.save()
        return HttpResponse('SuccessInsert')
    return HttpResponse('FailResponse')


def get_total_coins(request):
    '''
    获取一个学生的金币量
    调用方式GET
    @author 张彭豪
    @brief 从Student表中获取该学生的金币总量
    @param student_id 学生id
    @return coins 返回金币总量
    @return FailResponse获取金币总量失败
    '''
    if request.method == 'GET':
        student_id = request.GET.get('student_id')
        if student_id is not None:
            coins = Student.objects.filter(id=student_id).values('coin_total')[0]
            coins = coins['coin_total']
            return HttpResponse(coins)
    return HttpResponse('FailResponse')

def update_coins(request):
    '''
    更新金币总量
    调用方式POST
    @author 张彭豪
    @brief 在Student表中更新该学生的金币总量
    @param student_id 学生id
    @param newCoins 新增金币总量
    @return SuccessUpdate 金币总量更新成功
    @return FailResponse 金币总量更新失败
    '''
    if request.method == 'POST':
        param = json.loads(request.body.decode())
        if param is not None:
            student_id = param[0]
            newcoins = param[1]
            judge = Student.objects.filter(id=student_id).update(coin_total=newcoins)
            if judge != 0:
                return HttpResponse('SuccessUpdate')
    return HttpResponse('FailResponse')

def get_group_question(request):
    '''
    获取无限挑战的一组题
    调用方式POST
    @author 张彭豪
    @brief 通过传入的比赛id找到其对应的book_id,并获取获取相应数目的问题
    @param question_num 题目数量
    @param competition_id 比赛id
    @return question_list_store 返回题目生成列表
    @return FailResponse 获取题目列表失败
    '''
    if request.method == 'POST':
        param = json.loads(request.body.decode())
        question_num = param[0]
        competition_id = param[1]
        if competition_id == 0:
            return HttpResponse('FailResponse')
        question_set = []
        book_id = CompetitionInfo.objects.filter(
            id=competition_id
        ).values('book_id')[0]['book_id']
        question_list_store = []
        if book_id == 0:
            question_set = Question.objects.all()
            question_set = serializers.serialize('json', question_set, ensure_ascii=False)
            question_set = json.loads(question_set)
        else:
            word_set = Classification.objects.filter(category=book_id)
            for item in word_set:
                temp = serializers.serialize('json', \
                    Question.objects.filter(word=item.word), ensure_ascii=False)
                temp = json.loads(temp)
                question_set.extend(temp)
        i = 0
        while i < question_num:
            rand = random.randint(0, len(question_set) - 1)
            question_list_store.append(question_set[rand])
            i = i + 1
        question_list_store = json.dumps(question_list_store)
        return HttpResponse(question_list_store)
    return HttpResponse('FailResponse')

def add_infinite_challenge_log(request):
    '''
    添加无限挑战记录
    调用方式POST
    @author 陶磊
    @brief 将infinite_set相关的信息插入InfiniteChallengeLogbiao表，将student_id，competition_id，score相关的信息插入StudentHasCompetitionLog表
    @param infinite_set 存储无限挑战相关的信息，包括学生id，比赛id， 文体id，是否正确
    @param student_id 学生id
    @param competition_id 比赛id
    @param score 分数
    @return SuccessInsert 插入成功
    @return FailResponse 插入失败
    '''
    if request.method == 'POST':
        param = json.loads(request.body.decode())
        infinite_set = param[0]
        student_id = param[1]
        competition_id = param[2]
        score = param[3]
        for item in infinite_set:
            competition_item = InfiniteChallengeLog.objects.create(
                student_id=item['studentId'],
                competition_id=item['competitionId'],
                question_id=item['questionId'],
                is_right=item['isRight']
            )
            competition_item.save()
        judge = StudentHasCompetitionLog.objects.filter(competition_id=competition_id, student_id=student_id)
        if judge.exists():
            judge.update(score=score)
        else:
            log = StudentHasCompetitionLog.objects.create(
                student_id=student_id,
                competition_id=competition_id,
                score=score
            )
            log.save()
        return HttpResponse('SuccessInsert')
    return HttpResponse('FailResponse')

def new_competition(request):
    '''
    新建比赛
    调用方式POST
    @author 孙晓冰
    @brief 将比赛相关的所有信息插入CompetitionInfo表
    @param name 比赛名称
    @param organiser 组织者
    @param status 比赛状态
    @param create_time 创建时间
    @param begin_time 开始时间
    @param end_time 结束时间
    @param max_number 比赛最大参与人数
    @param type 比赛类型
    @param difficulty 比赛难度
    @param tool 是否允许使用道具
    @param zn_to_en 是否包含中译英
    @param en_to_zn 是否包含英译中
    @param listen_to_spelling 是否包含听力拼写
    @param listen_to_choose 是否包含听力选择
    @param coin_number 比赛门槛金币数
    @param book_id 比赛参考教材id
    @param top_number 比赛奖励前几名
    @param award 比赛前几名奖励多少金币
    @param classes 比赛所属班级
    @param school 比赛所属学校
    @param grade 比赛所属年级
    @return 您已成功新增比赛
    @return 所选教材不存在
    @return 新增班级失败
    '''
    if request.method == 'POST':
        competition_data = json.loads(request.body.decode())
        name = competition_data['name']
        organiser = competition_data['organiser']
        status = competition_data['status']
        create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        begin_time = competition_data['begin_time']
        end_time = competition_data['end_time']
        max_number = competition_data['max_number']
        type_ = competition_data['type']
        difficulty = competition_data['difficulty']
        tool = competition_data['tool']
        zn_to_en = competition_data['zn_to_en']
        en_to_zn = competition_data['en_to_zn']
        listen_to_spelling = competition_data['listen_to_spelling']
        listen_to_choose = competition_data['listen_to_choose']
        coin_number = competition_data['coin_number']
        book_id = competition_data['book_id']
        top_number = competition_data['top_number']
        award = competition_data['award']
        classes = competition_data['classes']
        school = competition_data['school']
        grade = competition_data['grade']
        if book_id != 0:
            competition_exist = Category.objects.filter(
                id=book_id
            )
            if competition_exist.count() == 0:
                return  HttpResponse('所选教材不存在')
        competition_data = CompetitionInfo.objects.create(
            name=name,
            organiser=organiser,
            status=status,
            create_time=create_time,
            begin_time=begin_time,
            end_time=end_time,
            max_number=max_number,
            type=type_,
            difficulty=difficulty,
            tool=tool,
            zn_to_en=zn_to_en,
            en_to_zn=en_to_zn,
            listen_to_spelling=listen_to_spelling,
            listen_to_choose=listen_to_choose,
            coin_number=coin_number,
            book_id=book_id,
            top_number=top_number,
            award=award,
            classes=classes,
            school=school,
            grade=grade
        )
        competition_data.save()
        return HttpResponse('您已成功新增比赛')
    return HttpResponse('新增比赛失败')

def get_competition_list_tophub(StudentHasCompetitionLogT, TOP):
    '''
    获取比赛的前几名
    @author 张彭豪
    @brief 从StudentHasCompetitionLogT表中取前TOP名的学生信息
    @param StudentHasCompetitionLogT 比赛信息表
    @param TOP 获取的前几名
    @return 包含id, student_name, avatar的前几名学生信息的字典数组
    '''
    order_student_set = StudentHasCompetitionLogT.objects.order_by('score')
    top_three = []
    tmp = {}
    k = 0
    while k < TOP:
        if k >= order_student_set.count():
            tmp['id'] = '-'
            tmp['student_name'] = '-'
            tmp['avatar'] = '-'
        else:
            tmp['id'] = order_student_set[k].student.id
            tmp['student_name'] = order_student_set[k].student.student_name
            tmp['avatar'] = order_student_set[k].student.avatar
        k = k + 1
        top_three.append(tmp)
    return top_three

def get_competition_list_loophub(competition_list, ite, TOP, student_id):
    '''
    获取比赛列表函数内的迭代函数
    @author 张彭豪
    @brief competition_list 比赛信息列表
    @param ite 迭代变量
    @param TOP 前几名
    @param student_id 学生id
    @return 无返回值
    '''
    INFINITE = 999
    dic = json.loads(
        serializers.serialize('json', CompetitionInfo.objects.filter(id=ite), \
            fields=('name', 'status', 'begin_time', 'end_time', 'type', \
                'book_id'), ensure_ascii=False))[0]
    book_id = dic['fields']['book_id']
    if book_id == 0:
        book_name = '不限教材'
    else:
        book_name = Category.objects.filter(id=book_id).values('category')
        if book_name.count() != 0:
            book_name = book_name[0]['category']
    dic['bookname'] = book_name
    dic['topThree'] = get_competition_list_tophub(StudentHasCompetitionLog, TOP)
    score = StudentHasCompetitionLog.objects.filter(student=student_id, competition=ite)
    if score.exists():
        score = score.values('score')[0]['score']
        rank = StudentHasCompetitionLog.objects.filter(score__gt=score, competition=ite).count() + 1
        dic['rank'] = rank
    else:
        dic['rank'] = INFINITE
    competition_list.append(dic)

def get_competition_list(request):
    '''
    获取比赛列表函数
    调用方式POST
    @author 孙晓冰
    @brief 获取某个学生的参加的和未参加的比赛信息
    @param student_id 学生id
    @return 比赛信息列表
    @return FailMessage 获取比赛信息失败
    '''
    TOP = 3
    if request.method == 'POST':
        student_id = json.loads(request.body.decode())
        competition_id_list = CompetitionInfo.objects.all().values('id')
        competition_id_list_taken = StudentHasCompetitionLog.objects.filter(
            student_id=student_id).values('competition_id')
        competition_id_list_set = set()
        competition_id_list_taken_set = set()
        i = 0
        while i < competition_id_list.count():
            competition_id_list_set.add(competition_id_list[i]['id'])
            i = i + 1
        i = 0
        while i < competition_id_list_taken.count():
            competition_id_list_taken_set.add(competition_id_list_taken[i]['competition_id'])
            i = i + 1
        competition_id_list_noset = competition_id_list_set - competition_id_list_taken_set
        competition_list_notaken = []
        competition_list_taken = []
        for ite in competition_id_list_noset:
            get_competition_list_loophub(competition_list_notaken, ite, TOP, student_id)
        for ite in competition_id_list_taken_set:
            get_competition_list_loophub(competition_list_taken, ite, TOP, student_id)
        param = {
            'takenlist': competition_list_taken,
            'notakenlist': competition_list_notaken
        }
        return HttpResponse(json.dumps(param))
    return HttpResponse('FailMessage')

def get_question(request):
    '''
    获取所有问题信息
    调用方式GET
    @author 陶磊
    @brief 获取所有问题信息
    @return 问题信息列表
    @return Get question failed 获取问题信息失败
    '''
    if request.method == 'GET':
        question = Question.objects.all()
        question = serializers.serialize('json', question, ensure_ascii=False)
        return HttpResponse(question)
    return HttpResponse('Get question failed')


def get_competition_info(request):
    '''
    获取某个比赛的信息
    调用方式GET
    @author 孙晓冰
    @brief 通过比赛id获取其相关信息
    @param competition_id 比赛id
    @return 返回比赛信息字典
    @return get_competition_info failed获取信息失败
    '''
    if request.method == 'GET':
        competition = CompetitionInfo.objects.filter(
            id=request.GET.get('competition_id')
        )
        competition_info = json.loads(
            serializers.serialize('json', competition, ensure_ascii=False)
        )
        return HttpResponse(json.dumps(competition_info))
    return HttpResponse('get_competition_info failed')

def all_competition_info(request):
    '''
    获取所有比赛信息
    调用方式GET
    @author 梁明唅
    @brief 获取所有比赛所有信息
    @return 所有比赛信息字典数组
    @return all_competition_info failed 获取比赛信息失败
    '''
    if request.method == 'GET':
        competition = CompetitionInfo.objects.all()
        competition_info = json.loads(
            serializers.serialize('json', competition, ensure_ascii=False)
        )
        return HttpResponse(json.dumps(competition_info))
    return HttpResponse('all_competition_info failed')

def get_competition_rank(request):
    '''
    获取比赛排名
    调用方式GET
    @author 梁明唅
    @brief 在StudentHasCompetitionLog表中获取按分数排名的学生信息
    @param competition_id 比赛信息
    @return 返回按分数从高到低的学生信息列表
    @return get_competition_rank_failed获取排名信息失败
    '''
    if request.method == 'GET':
        competition_id = request.GET.get('competition_id')
        rank_list = StudentHasCompetitionLog.objects.filter(competition=\
            competition_id).order_by('-score')
        res = []
        for rank_item in rank_list:
            item = Student.objects.filter(id=rank_item.student.id)
            name = item[0].student_name
            item = {'id': rank_item.student.id, 'name': name, 'score': rank_item.score}
            res.append(item)
        return HttpResponse(json.dumps(res), content_type='application/json')
    return HttpResponse('get_competition_rank_failed')

def edit_competition(request):
    '''
    编辑比赛信息
    调用方式POST
    @author 梁明唅
    @brief 根据比赛信息修改数据库里内容
    @param a_competition 一个比赛的所有信息
    @return edit_competition_success 编辑比赛成功
    @return edit_competition_failed 编辑比赛失败
    '''
    if request.method == 'POST':
        a_competition = json.loads(request.body.decode())
        CompetitionInfo.objects.\
        filter(id=a_competition['pk']).\
        update(name=a_competition['fields']['name'], \
        type=a_competition['fields']['type'], \
        organiser=a_competition['fields']['organiser'], \
        status=a_competition['fields']['status'], \
        grade=a_competition['fields']['grade'], \
        max_number=a_competition['fields']['max_number'])
        return HttpResponse('edit_competition_success')
    return HttpResponse('edit_competition_failed')

def prize_top(request):
    '''
    奖励前几名
    调用方式GET
    @author 梁明唅
    @brief 奖励前3名
    @param competition_id 比赛id
    @return prize_top_succeed 奖励成功
    @return prize_top_failed 奖励失败
    '''
    if request.method == 'GET':
        competition_id = request.GET.get('competition_id')
        CompetitionInfo.objects.filter(id=competition_id).update(status='finish')
        top_number = CompetitionInfo.objects.filter(id=competition_id).values('top_number')[0]['top_number']
        award = CompetitionInfo.objects.filter(id=competition_id).values('award')[0]['award']
        rank_list = StudentHasCompetitionLog.objects.filter(competition=\
            competition_id).order_by('-score')
        student_list = []
        index = 0
        for a_rank in rank_list:
            index += 1
            student_list.append(a_rank.student)
            if index == top_number:
                break
        for a_student in student_list:
            coin_total = Student.objects.filter(id=\
            a_student.id).values('coin_total')[0]['coin_total'] + award
            Student.objects.filter(id=a_student.id).update(coin_total=coin_total)
        return HttpResponse('prize_top_succeed')
    return HttpResponse('prize_top_failed')

def update_competiton_status():
    '''
    更新比赛状态
    @author 梁明唅
    @brief 每天更新今天结束的比赛状态为已结束
    '''
    today = time.strftime('%Y-%m-%d', time.localtime())
    CompetitionInfo.objects.filter(end_time=today).update(status='finish')
