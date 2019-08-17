'''
study应用下路由匹配模块
'''
from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('login_student', views.login_student, name='login_student'),
    path('login_teacher', views.login_teacher, name='login_teacher'),
    path('index', views.index, name='index'),
    path('leader_board', views.leader_board, name='leader_board'),
    path('add_new_class', views.add_new_class, name='add_new_class'),
    path('teacher_classes/', views.teacher_classes, name='teacher_classes'),
    path('add_new_student', views.add_new_student, name='add_new_student'),
    path('teacher_delete_classes/', views.teacher_delete_classes, name='teacher_delete_classes'),
    path('teacher_students/', views.teacher_students, name='teacher_students'),
    path('teacher_delete_students/', views.teacher_delete_students, name='teacher_delete_students'),
    path('get_user_info', views.get_user_info, name='get_user_info'),
    path('update_info', views.update_info, name='update_info'),
    path('get_student_classes', views.get_student_classes, name='get_student_classes')
]
