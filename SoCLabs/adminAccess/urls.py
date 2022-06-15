from django import views
from django.urls import path, re_path
from .views import *

urlpatterns = [
    # path('test', timeConfigFunc, name='TimeConfig'),
    re_path(r'(?P<pk>\d+)/$', index, name='TimeConfig'),
]
