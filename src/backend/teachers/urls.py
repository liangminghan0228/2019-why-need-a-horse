'''
TeacherBuiltIn应用路由匹配模块
'''
from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('change_password', views.change_password, name='change_password'),
]
