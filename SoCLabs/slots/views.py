from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import TimeSchedule,TimeSlot
from django.utils import timezone
from datetime import date, timedelta

DAYS_OF_WEEK = {
    'Friday':0,
    'Saturday':1,
    'Sunday':2,
    'Monday':3,
    'Tuesday':4,
    'Wednesday':5,
    'Thursday':6
}

def bookSlots(request):
    
    # making a list of all days left in the lab week
    date_now = date.today()
    day_now = date_now.weekday()
    d = 7 - DAYS_OF_WEEK[day_now]
    i=1
    days = [date_now,]
    while i<d:
        days.append(date.today + timedelta(days=i))

    context = {
        'days':days,
        'time_slots': TimeSchedule.objects.filter(day=date_now).all() 
    }    
    return render(request,'slots/booking.html')
