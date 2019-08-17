'''
study应用路由匹配模块
'''
from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('get_word', views.get_word, name='get_word'),
    path('leader_board', views.leader_board, name='leader_board'),
    path('student_statistic', views.get_statistic_with_student_id, name='student_statistic'),
    path('leader_coin_board', views.leader_coin_board, name='leader_coin_board'),
    path('leader_today_board', views.leader_today_board, name='leader_today_board'),
    path('leader_all_board', views.leader_all_board, name='leader_all_board'),
    path('get_study_statistic', views.get_study_statistic, name='get_study_statistic'),
    path('get_unit_list', views.get_unit_list, name='get_unit_list'),
    path('get_study_date', views.get_study_date, name='get_study_date'),
    path('card_today', views.card_today, name='card_today'),
    path('register_course', views.register_course, name='register_course'),
    path('get_opened_course', views.get_opened_course, name='get_opened_course'),
    path('get_current_course', views.get_current_course, name='get_current_course'),
    path('change_course', views.change_course, name='change_course'),
    path('get_pretest_word', views.get_pretest_word, name='get_pretest_word'),
    path('set_word_rank', views.set_word_rank, name='set_word_rank'),
    path('set_word_status', views.set_word_status, name='set_word_status'),
    path('show_register_result', views.show_register_result, name='show_register_result'),
    path('get_bar_statistic', views.get_bar_statistic, name='get_bar_statistic'),
    path('add_pretest_log', views.add_pretest_log, name='add_pretest_log'),
    path('add_test_log', views.add_test_log, name='add_test_log'),
    path('get_after_test', views.get_after_test, name='get_after_test'),
    path('get_book_test', views.get_book_test, name='get_book_test'),
    path('get_review_test', views.get_review_test, name='get_review_test'),
    path('teacher_test_record', views.teacher_test_record, name='teacher_test_record'),
    path('get_study_statistic_seven',
         views.get_study_statistic_seven, name='get_study_statistic_seven'),
    path('get_test_score', views.get_test_score, name='get_test_score'),
    path('update_unit_status', views.update_unit_status, name='update_unit_status')
]
