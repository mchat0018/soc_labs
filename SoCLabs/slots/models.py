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
HOUR_SLOTS = []
for i in range(24):
    HOUR_SLOTS.append((str(i).zfill(2),str(i).zfill(2)))

HOUR_SLOTS = tuple(HOUR_SLOTS)
MINUTE_SLOTS = []
for i in range(60):
    MINUTE_SLOTS.append((str(i).zfill(2),str(i).zfill(2)))
MINUTE_SLOTS = tuple(MINUTE_SLOTS)

# class DaySchedule(models.Model):
#     day = models.CharField(max_length=10,choices=DAYS_OF_WEEK)

class TimeConfig(models.Model):
    day = models.CharField(max_length=10,choices=DAYS_OF_WEEK,null=True)
    start_time_hours = models.CharField(max_length=2,choices=HOUR_SLOTS,null=True)
    start_time_minutes = models.CharField(max_length=2,choices=MINUTE_SLOTS,null=True)
    end_time_hours = models.CharField(max_length=2,choices=HOUR_SLOTS,null=True)
    end_time_minutes = models.CharField(max_length=2,choices=MINUTE_SLOTS,null=True)
    duration = models.IntegerField(null=True)
    no_of_boards = models.IntegerField(default=10)

    def __str__(self):
        return f'{self.day};Slots from {self.start_time_hours}:{self.start_time_minutes} to {self.end_time_hours}:{self.end_time_minutes};duration:{self.duration} minutes'
        
class TimeSlot(models.Model):
    start_time_hours = models.CharField(max_length=2,choices=HOUR_SLOTS,null=True)
    start_time_minutes = models.CharField(max_length=2,choices=MINUTE_SLOTS,null=True)
    end_time_hours = models.CharField(max_length=2,choices=HOUR_SLOTS,null=True)
    end_time_minutes = models.CharField(max_length=2,choices=MINUTE_SLOTS,null=True)

    def __str__(self):
        return f'{self.start_time_hours}:{self.start_time_minutes} - {self.end_time_hours}:{self.end_time_minutes}'

class TimeSchedule(models.Model):
    day = models.CharField(max_length=10,choices=DAYS_OF_WEEK)
    time_slot = models.ForeignKey(TimeSlot,on_delete=models.CASCADE)
    time_config = models.ForeignKey(TimeConfig,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return f'{self.day},{self.time_slot.start_time_hours}:{self.time_slot.start_time_minutes} - {self.time_slot.end_time_hours}:{self.time_slot.end_time_minutes}'

class Board(models.Model):
    board = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    day = models.CharField(max_length=10,choices=DAYS_OF_WEEK,null=True)
    time_slot = models.ForeignKey(TimeSlot,on_delete=models.CASCADE,null=True)
    time_sched = models.ForeignKey(TimeSchedule,on_delete=models.CASCADE,null=True)

    def __str__(self):
        board_no = self.id % self.time_sched.time_config.no_of_boards
        return f'Board{board_no} for {self.day},{self.time_slot.start_time_hours}:{self.time_slot.start_time_minutes} - {self.time_slot.end_time_hours}:{self.time_slot.end_time_minutes}'