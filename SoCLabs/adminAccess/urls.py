from django.urls import path,include
from .views import *

urlpatterns = [
    path('config/board_select/',board_page,name='edit-board'),
    path('config/time_select/', crud, name='edit-time'),
    path('config/adminRts/', adminRts, name='adminRts'),
    path("config/delete/<int:pk>/", delete_config2, name='delete_config2'),
    path("config/delete/<int:pk>/", delete_config, name='delete_config'),
    path('reset/', reset, name='reset'),
]