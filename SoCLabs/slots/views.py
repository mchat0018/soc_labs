from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.template import RequestContext
from .models import TimeSchedule,Board
from django.utils import timezone
from datetime import date, timedelta

DAYS_OF_WEEK = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

def bookSlots(request):
    date_now = date.today()
    day_now = date_now.weekday()
    today = DAYS_OF_WEEK[day_now]
    # making a list of all days left in the lab week
    days = []
    i = day_now
    while i<7:
        days.append(DAYS_OF_WEEK[i])
        i+=1
    
    selected_day = ''
    
    if request.method == 'POST':
        if 'select_day' in request.POST:
            selected_day = request.POST['select_day'] 
        elif 'select_time' in request.POST:
            selected_day = today
    else:
        selected_day = today

    data = {
        'days': days,
        'time_schedules': TimeSchedule.objects.filter(day=selected_day).all(),
        'boards': Board.objects.filter(day=selected_day).all() 
    }    
    return render(request,'slots/booking.html',context = data)
