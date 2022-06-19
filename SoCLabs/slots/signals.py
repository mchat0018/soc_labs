from django.db.models.signals import post_save
from django.contrib.auth.models import User 
from django.dispatch import receiver
from .models import *

@receiver(post_save,sender=TimeConfig)
def create_TimeSlots(sender,instance,created,**kwargs):
    if created:
        start_time_hours = int(instance.start_time_hours)
        start_time_minutes = int(instance.start_time_minutes)
        end_time_hours = int(instance.end_time_hours)
        end_time_minutes = int(instance.end_time_minutes)
        duration = instance.duration

        if start_time_hours>=end_time_hours:
            end_time_hours += 24

        start = int(start_time_hours)*60 + int(start_time_minutes)
        end = int(end_time_hours)*60 + int(end_time_minutes)
        no_of_slots = (end-start)//duration

        st_h = str(start_time_hours).zfill(2)
        st_m = str(start_time_minutes).zfill(2)
       
        for i in range(no_of_slots):
            ed = start + duration
            ed_h = (ed//60)
            if(ed_h>24):
                ed_h = ed_h - 24
            ed_h = str(ed_h).zfill(2)
            ed_m = str(ed%60).zfill(2)
            
            time_slot,done = TimeSlot.objects.get_or_create(start_time_hours = st_h,start_time_minutes = st_m,end_time_hours = ed_h,end_time_minutes = ed_m)
            day = instance.day
            time_schedule = TimeSchedule.objects.create(day=day,time_slot=time_slot,time_config=instance,course=instance.course)
            
            boards = IPAddress.objects.filter(course=instance.course).all()
            for board in boards:
                slot = Board.objects.create(day = day,time_slot=time_slot,board_name=board.board_name,ip_addr=board,course=instance.course)
          
            st_h = ed_h
            st_m = ed_m
            start = int(st_h)*60 + int(st_m)
            
@receiver(post_save,sender=IPAddress)
def create_boards(sender,instance,created,**kwargs):
    course = instance.course
    
    if not created:
        # if the IPAddress object was updated, delete the earlier slots referencing the same object
        Board.objects.filter(board_name=instance.board_name).delete()

    if course is not None:
        # creating new slots from the created/updated board
        time_configs = TimeConfig.objects.filter(course=course).all()
        for time_config in time_configs.all():
            time_scheds = TimeSchedule.objects.filter(time_config=time_config).all()
            for time_sched in time_scheds.all():
                board,_= Board.objects.get_or_create(day=time_sched.day,time_slot=time_sched.time_slot,
                                        board_name=instance.board_name,ip_addr=instance,course=course)
