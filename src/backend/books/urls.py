from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('get_word', views.get_word, name='get_word'),
    path('generate_question', views.generate_question, name='generate_question'),
    path('generate_unit_word', views.generate_unit_word, name='generate_unit_word'),
    path('get_courses', views.get_courses, name='get_courses'),
    path('get_book_name', views.get_book_name, name='get_book_name'),
    path('get_course_info', views.get_course_info, name='get_course_info')
]
