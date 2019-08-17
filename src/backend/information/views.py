'''
information应用路由处理函数模块
'''
import json
import time
import os
from django.conf import settings
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.hashers import make_password, check_password
from .models import StudentBuiltIn, Student, Classes
from teachers.models import TeacherBuiltIn
from django.http import JsonResponse


def index(request):
    '''
    生成学生教师账号测试数据
    调用方式 GET
    @author 陶磊
    @return Insert account into db success 生成数据成功
    @return Insert account into db failed 访问失败
    '''
    if request.method == 'GET':
        classes = Classes(
            classes_description='class one',
            student_number=123,
            class_name='class one'
        )
        classes.save()
        stu = Student(
            id='12345',
            student_name='stone',
            login_times=2019,
            coin_total=100,
            classes=classes,
            register_time='2019-11-11',
            avatar='avatar',
            vocabularies=123,
            cumulative_study_duration=1234,
            last_login='2019-11-11 01:26',
            grade=3,
            school='NKU'
        )
        stu.save()
        user = StudentBuiltIn(
            password=make_password('12345', None, 'pbkdf2_sha256'),
            student=stu
        )
        user.save()
        teacher = TeacherBuiltIn(
            username='begin',
            password=make_password('12345', None, 'pbkdf2_sha256')
        )
        teacher.save()
        return HttpResponse('Insert account into db success')
    return HttpResponse('Insert account into db failed')


def login_student(request):
    '''
    学生端用户登录
    调用方式 POST
    @author 陶磊
    @param username 学生id
    @param password 密码
    @return loginStudentSuccess 登录成功
    @return loginStudentFailed 登录失败
    '''
    if request.method == 'POST':
        student_id = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if student_id and password:
            user = StudentBuiltIn.objects.filter(student_id__exact=student_id)
            search_result = json.loads(serializers.serialize(
                'json', user, ensure_ascii=False))
            if search_result:
                check_pass = search_result[0]['fields']['password']
            else:
                return HttpResponse('loginStudentFailed')
            if check_password(password, check_pass):
                request.session['student_id'] = student_id
                return HttpResponse('loginStudentSuccess')
    return HttpResponse('loginStudentFailed')


def login_teacher(request):
    '''
    教师端用户登录
    调用方式 POST
    @author 陶磊
    @param username 用户名
    @param password 密码
    @return loginTeacherSuccess 登录成功
    @return loginTeacherFailed 登录失败
    '''
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if username and password:
            user = TeacherBuiltIn.objects.filter(username__exact=username)
            search_result = json.loads(serializers.serialize(
                'json', user, ensure_ascii=False))
            if search_result:
                check_pass = search_result[0]['fields']['password']
            else:
                return HttpResponse('loginTeacherFailed')
            if check_password(password, check_pass):
                request.session['teacher_id'] = username
                return HttpResponse('loginTeacherSuccess')
    return HttpResponse('loginTeacherFailed')


def leader_board():
    '''
    暂无
    '''


def add_new_student(request):
    '''
    根据班级id和学生id在相应班级里添加新学生
    调用方式 POST
    @author 梁明晗
    @param currClass 班级id
    @param studentInfo 学生信息
    @param id 学生id
    @return 该ID已存在，请勿重复！ 添加失败
    @return SuccessCreateStudent 创建成功
    @return FailedCreateStudent 创建失败
    '''
    if request.method == 'POST':
        param = json.loads(request.body.decode())
        class_id = param[0]['currClass']
        student_info = param[1]['studentInfo']
        student_id = student_info['id']
        queryset = Student.objects.filter(id=student_id)
        if queryset.exists():
            return HttpResponse('该ID已存在，请勿重复！')
        else:
            student_name = student_info['name']
            student_email = student_info['email']
            student_password = student_info['password']
            pay_status = student_info['status']
            grade = student_info['grade']
            school = student_info['school']
            student_instance = Student.objects.create(
                id=student_id,
                student_name=student_name,
                email=student_email,
                login_times=0,
                coin_total=0,
                register_time=time.strftime('%Y-%m-%d', time.localtime()),
                pay_status=pay_status,
                vocabularies=0,
                cumulative_study_duration=0,
                grade=grade,
                school=school,
                last_login=time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.localtime()),
                classes_id=class_id
            )
            student_instance.save()
            student_built_in_instance = StudentBuiltIn.objects.create(
                student_id=student_id, password=make_password(student_password))
            student_built_in_instance.save()
            return HttpResponse('SuccessCreateStudent')
    return HttpResponse('FailedCreateStudent')


def teacher_students(request):
    '''
    教师端获取所有学生信息
    调用方式 GET
    @author 梁明晗
    @return student_info 所有学生信息
    @return Teacher_students failed 获取失败
    '''
    if request.method == 'GET':
        student_info = Student.objects.all()
        student_info = serializers.serialize(
            'json', student_info, ensure_ascii=False)
        student_info = json.loads(student_info)
        return JsonResponse(student_info, safe=False)
    return HttpResponse('Teacher_students failed')


def teacher_delete_students(request):
    '''
    教师端根据班级id和学生id在相应班级里删除学生
    调用方式 POST
    @author 梁明晗
    @param currClass 班级id
    @param studentInfo 学生信息
    @param pk 学生id
    @return student_info 学生信息
    @return delete_students_failed 删除失败
    '''
    if request.method == 'POST':
        deleted_students = json.loads(request.body.decode())
        Student.objects.get(id=deleted_students['pk']).delete()
        student_info = Student.objects.all()
        student_info = serializers.serialize(
            'json', student_info, ensure_ascii=False)
        student_info = json.loads(student_info)
        return JsonResponse(student_info, safe=False)
    return HttpResponse('delete_students_failed')


def teacher_classes(request):
    '''
    教师端获取所有班级信息
    调用方式 GET
    @author 梁明晗
    @return class_info 班级信息
    @return Teacher_classes failed 获取失败
    '''
    if request.method == 'GET':
        class_info = Classes.objects.all()
        class_info = serializers.serialize(
            'json', class_info, ensure_ascii=False)
        class_info = json.loads(class_info)
        return JsonResponse(class_info, safe=False)
    return HttpResponse('Teacher_classes failed')


def teacher_delete_classes(request):
    '''
    教师端删除选中班级，返回删除后所有班级信息
    调用方式 POST
    @author 梁明晗
    @param pk 班级id
    @return class_info 班级信息
    @return Teacher_classes failed 获取失败
    '''
    if request.method == 'POST':
        deleted_classes = json.loads(request.body.decode())
        Classes.objects.get(id=deleted_classes['pk']).delete()
        classes_info = Classes.objects.all()
        classes_info = serializers.serialize(
            'json', classes_info, ensure_ascii=False)
        classes_info = json.loads(classes_info)
        return JsonResponse(classes_info, safe=False)
    return HttpResponse('delete_classes_failed')


def add_new_class(request):
    '''
    教师端增添班级
    调用方式 POST
    @author 梁明晗
    @param className 班级名称
    @param introduce 班级介绍
    @return 该班级已存在,请勿重复！ 新增失败
    @return SuccessCreateClass 新增成功
    @return FailedCreateClass 新增失败
    '''
    if request.method == 'POST':
        class_data = json.loads(request.body.decode())
        classname = class_data['className']
        introduce = class_data['introduce']
        queryset = Classes.objects.filter(class_name=classname)
        if queryset.exists():
            return HttpResponse('该班级已存在,请勿重复！')
        else:
            class_data = Classes.objects.create(
                class_name=classname, classes_description=introduce, student_number=0)
            class_data.save()
            return HttpResponse('SuccessCreateClass')
    return HttpResponse('FailedCreateClass')


def get_user_info(request):
    '''
    教师端获取学生信息
    调用方式 GET
    @author 陶磊
    @param  student_id 学生id
    @return user_info 用户信息
    '''
    student_id = request.GET.get('student_id')
    user_info_set = Student.objects.filter(id=student_id)
    user_info = serializers.serialize(
        'json', user_info_set, ensure_ascii=False)
    return HttpResponse(user_info)


def update_info(request):
    '''
    学生更新用户信息
    调用方式 GET
    @author 陶磊
    @param student_id 学生id
    @param student_name 学生名称
    @param avatar 头像
    @return upload over! 更新成功
    '''
    student_id = request.GET.get('student_id')
    student_name = request.GET.get('student_name')
    avatar = request.FILES.get('avatar', None)
    name = str(int(time.time())) + avatar.name
    if not avatar:
        return HttpResponse('no files for upload!')
    media_path = settings.MEDIA_ROOT
    destination = open(os.path.join(media_path, name), 'wb+')
    for chunk in avatar.chunks():
        destination.write(chunk)
    destination.close()
    Student.objects.filter(id=student_id).update(
        student_name=student_name, avatar=os.path.join(media_path, name))
    return HttpResponse('upload over!')


def get_student_classes(request):
    '''
    根据学生id获取所在班级信息
    调用方式 GET
    @author 梁明晗
    @param student_id 学生id
    @return user_classes 学生所在班级信息
    '''
    student_id = request.GET.get('student_id')
    user_info_set = Student.objects.get(id=student_id)
    user_classes = user_info_set.classes.class_name
    return HttpResponse(user_classes)
