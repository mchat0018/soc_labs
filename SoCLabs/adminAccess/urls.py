from django.urls import path,include
from .views import *

urlpatterns = [
    path('config/',admin_page,name='edit-config'),
    path('', crud, name='crud-config'),
    path("delete/<int:pk>/", delete_config, name='delete-config'),
]