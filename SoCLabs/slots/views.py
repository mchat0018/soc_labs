from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from .models import TimeSchedule,TimeSlot,TimeConfig,Board
from django.utils import timezone
from datetime import date, timedelta
import json

DAYS_OF_WEEK = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

def bookSlots(request):
    # making a list of all days left in the lab week
    date_now = date.today()
    day_now = date_now.weekday()
    days = []
    i = day_now
    while i<7:
        days.append(DAYS_OF_WEEK[i])
        i+=1

    data = {
        'days': days,
        'time_schedules': TimeSchedule.objects.filter(day=days[day_now]).all(),
        'boards': Board.objects.all(day=days[day_now]) 
    }    
    return render(request,'slots/booking.html',context = data)
