from django.urls import path,include
from .views import *

urlpatterns = [
    path('', adminRts, name='adminRts'),
    path("delete/<int:pk>/", delete_config2, name='delete_config2'),
    path('unenroll/<int:pk>/', unenroll, name='unenroll'),
    path('reset/', reset, name='reset'),
    path('registerCSV/', registerCSV, name='registerCSV'),
]