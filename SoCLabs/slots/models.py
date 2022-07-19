from ipaddress import ip_address
from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.db.models.fields import DateField
from django.db.models.fields.related import ForeignKey
from courses.models import Course

INDEXED_DAYS = (
    (0,'Monday'),
    (1,'Tuesday'),
    (2,'Wednesday'),
    (3,'Thursday'),
    (4,'Friday'),
    (5,'Saturday'),
    (6,'Sunday')
)

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

BOARD_TYPES = (
    ('Basys3','Basys3'),
    ('Zynq','Zynq'),
    ('Zedboard','Zedboard')
)

class StartDay(models.Model):
    day = models.IntegerField(default=0, choices=INDEXED_DAYS)
    course = models.OneToOneField(Course,on_delete=models.CASCADE)

class TimeConfig(models.Model):
    day = models.CharField(max_length=10,choices=DAYS_OF_WEEK,null=True)
    start_time_hours = models.CharField(max_length=2,choices=HOUR_SLOTS,null=True)
    start_time_minutes = models.CharField(max_length=2,choices=MINUTE_SLOTS,null=True)
    end_time_hours = models.CharField(max_length=2,choices=HOUR_SLOTS,null=True)
    end_time_minutes = models.CharField(max_length=2,choices=MINUTE_SLOTS,null=True)
    duration = models.IntegerField(null=True)
    slot_limit = models.IntegerField(default=5)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return f'{self.course};{self.day};Slots from {self.start_time_hours}:{self.start_time_minutes} to {self.end_time_hours}:{self.end_time_minutes};duration:{self.duration} minutes'
        
class TimeSlot(models.Model):
    start_time_hours = models.CharField(max_length=2,choices=HOUR_SLOTS,null=True)
    start_time_minutes = models.CharField(max_length=2,choices=MINUTE_SLOTS,null=True)
    end_time_hours = models.CharField(max_length=2,choices=HOUR_SLOTS,null=True)
    end_time_minutes = models.CharField(max_length=2,choices=MINUTE_SLOTS,null=True)

    time_config = models.ForeignKey(TimeConfig,on_delete=models.CASCADE,null=True)
    # course = models.ForeignKey(Course,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return f'{self.start_time_hours}:{self.start_time_minutes} - {self.end_time_hours}:{self.end_time_minutes}'

class TimeSchedule(models.Model):
    day = models.CharField(max_length=10,choices=DAYS_OF_WEEK)
    time_slot = models.ForeignKey(TimeSlot,on_delete=models.CASCADE)
    time_config = models.ForeignKey(TimeConfig,on_delete=models.CASCADE,null=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return f'{self.course};{self.day};{self.time_slot.start_time_hours}:{self.time_slot.start_time_minutes}-{self.time_slot.end_time_hours}:{self.time_slot.end_time_minutes}'

class IPAddress(models.Model):
    # board_no = models.IntegerField(default=1)
    board_serial = models.CharField(max_length=60,null=True)
    board_type = models.CharField(max_length=10,choices=BOARD_TYPES,null=True)
    board_name = models.CharField(max_length=12,null=True)
    ip = models.GenericIPAddressField(protocol='both',null=True)
    cam_port = models.CharField(max_length=6,null=True)
    arduino_pin = models.IntegerField(default=1,null=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return f'IPv4 for {self.board_name}:{self.ip}'

class Board(models.Model):
    board_user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    day = models.CharField(max_length=10,choices=DAYS_OF_WEEK,null=True)
    time_slot = models.ForeignKey(TimeSlot,on_delete=models.CASCADE,null=True)

    time_sched = models.ForeignKey(TimeSchedule,on_delete=models.CASCADE,null=True)

    board_name = models.CharField(max_length=12,null=True)
    ip_addr = models.ForeignKey(IPAddress,on_delete=models.SET_NULL,null=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    
    def __str__(self):
        return f'{self.board_name} for {self.day},{self.time_slot.start_time_hours}:{self.time_slot.start_time_minutes} - {self.time_slot.end_time_hours}:{self.time_slot.end_time_minutes}'
    