from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.db.models.fields import DateField
from django.db.models.fields.related import ForeignKey

DAYS_OF_WEEK = (
    ('Monday','Monday'),
    ('Tuesday','Tuesday'),
    ('Wednesday','Wednesday'),
    ('Thursday','Thursday'),
    ('Friday','Friday'),
    ('Saturday','Saturday'),
    ('Sunday','Sunday')
)
# TIME_SLOTS = (
#     ('00:00 - 00:30'),

# )
HOUR_SLOTS = []
for i in range(24):
    HOUR_SLOTS.append((i,str(i)))

HOUR_SLOTS = tuple(HOUR_SLOTS)
MINUTE_SLOTS = []
for i in range(60):
    MINUTE_SLOTS.append((i,str(i).zfill(2)))
MINUTE_SLOTS = tuple(MINUTE_SLOTS)

# class DaySchedule(models.Model):
#     day = models.CharField(max_length=10,choices=DAYS_OF_WEEK)

class TimeSlot(models.Model):
    start_time_hours = models.CharField(max_length=2,choices=HOUR_SLOTS,null=True)
    start_time_minutes = models.CharField(max_length=2,choices=MINUTE_SLOTS,null=True)
    end_time_hours = models.CharField(max_length=2,choices=HOUR_SLOTS,null=True)
    end_time_minutes = models.CharField(max_length=2,choices=MINUTE_SLOTS,null=True)

class TimeSchedule(models.Model):
    day = models.DateField(null=True,blank=False)
    time_slot = models.ForeignKey(TimeSlot,on_delete=models.CASCADE)
    board1 = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,related_name='board1_user')
    board2 = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,related_name='board2_user')
    board3 = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,related_name='board3_user')
    board4 = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,related_name='board4_user')
    board5 = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,related_name='board5_user')
    board6 = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,related_name='board6_user')
    board7 = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,related_name='board7_user')
    board8 = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,related_name='board8_user')
    board9 = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,related_name='board9_user')
    board10 = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,related_name='board10_user')
