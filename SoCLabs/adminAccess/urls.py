from django.urls import path,include
from .views import *

urlpatterns = [
    path('config/board_select/',board_page,name='edit-board'),
    path('config/time_select/', crud, name='edit-time'),
    path("config/delete/<int:pk>/", delete_config, name='delete_config'),
]