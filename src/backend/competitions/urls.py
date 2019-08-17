from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('new_competition', views.new_competition, name='new_competition'),
    path('get_question', views.get_question, name='get_question'),
    path('get_competition_info', views.get_competition_info, name='get_competition_info'),
    path('get_competition_list', views.get_competition_list, name='get_competition_list'),
    path('all_competition_info', views.all_competition_info, name='all_competition_info'),
    path('get_competition_rank', views.get_competition_rank, name='get_competition_rank'),
    path('edit_competition', views.edit_competition, name='edit_competition'),
    path('prize_top', views.prize_top, name='prize_top'),
    path('get_group_question', views.get_group_question, name='get_group_question'),
    path('add_infinite_challenge_log', views.add_infinite_challenge_log, name='add_infinite_challenge_log'),
    path('get_total_coins', views.get_total_coins, name='get_total_coins'),
    path('update_coins', views.update_coins, name='update_coins'),
    path('get_pk_data', views.get_pk_data, name='get_pk_data'),
    path('add_pk_log', views.add_pk_log, name='add_pk_log'),
    path('generate_pk_ghost_log', views.generate_pk_ghost_log, name='generate_pk_ghost_log')
]
