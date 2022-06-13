from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Profile
from slots.models import Board,TimeConfig,TimeSchedule,TimeSlot
from .forms import UserRegisterForm,UserUpdateForm,ProfileForm
from datetime import datetime
import time
import pytz

DAYS_OF_WEEK = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
day_dict={
    'Monday':0,
    'Tuesday':1,
    'Wednesday':2,
    'Thursday':3,
    'Friday':4,
    'Saturday':5,
    'Sunday':6
}

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Account created for {username}. You can now login!')
            return redirect('login')

    else:
        form = UserRegisterForm
        
    context = {
        'form':form
    }
    
    return render(request,'users/register.html',context)

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileForm(request.user,request.FILES,instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'Your profile has been updated')
            
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileForm(instance=request.user.profile)
    
    # getting current day and time
    ist = pytz.timezone('Asia/Kolkata')
    datetime_now = datetime.now(ist)
    curr_time = datetime_now.strftime('%H:%M')
    curr_time_hours,curr_time_minutes = tuple(curr_time.split(':'))
    curr_day = datetime.today().weekday()
    today = DAYS_OF_WEEK[curr_day]
    print(curr_time)
    # getting available time slots and days
    crit = (Q(end_time_hours__gt=curr_time_hours) | (Q(end_time_hours=curr_time_hours) & Q(end_time_minutes__gt=curr_time_minutes)))
    timeslots = TimeSlot.objects.filter(crit).all()
    # getting the remaining booked slots for today
    booked_slots = Board.objects.filter(board_user=request.user).filter(day=today).filter(time_slot__in=timeslots).all()
    booked_slots = list(booked_slots)
    # getting the booked time slots for the remaining days of the lab week
    if curr_day != 6:
        days = DAYS_OF_WEEK[curr_day+1:]
        booked_slots += list(Board.objects.filter(board_user=request.user).filter(day__in=days).all())
    # sorting the booked slots
    booked_slots.sort(key=lambda x: str(day_dict[x.day]+1)+x.time_slot.start_time_hours+x.time_slot.start_time_minutes, reverse=False)
    
    for slot in booked_slots:
        print(slot)
    
    context = {
        'u_form':u_form,
        'p_form':p_form,
        'booked_slots':booked_slots,
        'curr_time_hours':curr_time_hours,
        'curr_time_minutes':curr_time_minutes,
        'curr_day':DAYS_OF_WEEK[curr_day]
    }
    return render(request,'users/profile.html',context)