from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from .models import TimeSchedule,TimeSlot,TimeConfig
from django.utils import timezone
from datetime import date, timedelta
import json

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
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # making a list of all days left in the lab week
        date_now = date.today()
        day_now = date_now.weekday()
        i=DAYS_OF_WEEK[day_now]
        days = [day_now,]
        while i<7:
            days.append(DAYS_OF_WEEK.keys(DAYS_OF_WEEK.values().index(i)))
            i+=1

        context = {
            'days': days,
            'time_schedule': TimeSchedule.objects.filter(day=day_now).all() 
        }    
        return JsonResponse(context)
        # return render(request,'slots/booking.html',context)
