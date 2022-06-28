from django.urls import path,include
from .views import *

urlpatterns = [
    path('',course_page,name='course-page'),
    path('lab/<lab_no>/',lab_page,name='lab-page'),
    path('courseInfo/', courseInfo, name='courseInfo'),
    path('deleteLab/<lab_id>/', deleteLab, name='deleteLab'),
    path('updateCourseDes/', updateCourseDes, name='updateCourseDes'),
    path('bookslots/',include('slots.urls')),
    path('camview/',include('webcam.urls')),
    path('adminPage/',include('adminAccess.urls'))
]