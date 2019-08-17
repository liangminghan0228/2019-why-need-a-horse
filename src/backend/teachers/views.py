'''
TeacherBuiltIn应用路由处理函数模块
'''
from teachers.models import TeacherBuiltIn
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.core import serializers
import json

def change_password(request):
    '''
    改变教师密码
    调用方式POST
    @param username 教师用户名
    @param password 旧密码
    @param new_password 新密码
    @return modifyPasswordSuccess 修改成功
    @return modifyPasswordFaided 修改失败
    '''
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('oldpass', None)
        new_password = request.POST.get('newpass', None)
        if username and password:
            user = TeacherBuiltIn.objects.filter(username__exact=username)
            search_result = json.loads(serializers.serialize('json', user, ensure_ascii=False))
            if search_result:
                verify_pass = search_result[0]['fields']['password']
            else:
                return HttpResponse('modifyPasswordFailed')
            if check_password(password, verify_pass):
                password = make_password(new_password, None, 'pbkdf2_sha256')
                user.update(password=password)
                return HttpResponse('modifyPasswordSuccess')
    return HttpResponse('modifyPasswordFaided')
