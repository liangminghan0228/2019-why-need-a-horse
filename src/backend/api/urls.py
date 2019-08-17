from django.contrib import admin
from django.urls import path, include

from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', include('books.urls')),
    path('information/', include('information.urls')),
    path('study/', include('study.urls')),
    path('competitions/', include('competitions.urls')),
    path('teachers/', include('teachers.urls'))
]
