from django.urls import path,include
from .views import *

urlpatterns = [
    path('config/',admin_page,name='edit-config'),
]