from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from .models import TimeConfig, TimeSchedule,Board,TimeSlot
from django.utils import timezone
from datetime import date, timedelta, datetime
import pytz

DAYS_OF_WEEK = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

@login_required
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
    
    selected_day = today
    
    if request.method == 'POST':
        for key,value in request.POST.lists():
            print(key,value)
            
        if 'select_day' in request.POST:
            selected_day = request.POST['days'] 
        
        elif 'select_time' in request.POST:
            time_slot = request.POST.get('time-slot',None)
            board = request.POST.get('board',None)
            selected_day = request.POST.get('selected_day',None)
            
            if time_slot is not None and board is not None:
                # checking if slot limit for the day has been reached
                slot_limit = TimeConfig.objects.filter(day=selected_day).first().slot_limit
                slots_booked = len(Board.objects.filter(board_user=request.user).filter(day=selected_day).all())
                
                if(slot_limit<=slots_booked): messages.error(request,f'Failure to book slot. Slot limit for the day already been reached')
                else:
                # retrieving the TimeSlot object
                    start_time,end_time = tuple(time_slot.replace(' ','').split('-'))
                    start_time_hours,start_time_minutes = tuple(start_time.split(':'))
                    end_time_hours,end_time_minutes = tuple(end_time.split(':'))
                    
                    # getting the current time
                    datetime_now = datetime.now(pytz.timezone('Asia/Kolkata'))
                    curr_time = datetime_now.strftime('%H:%M')
                    # if the time slot booked is a previous time slot, it shouldn't be able to book
                    if(curr_time>=end_time): messages.error(request,f'Failure to book slot. Please book a pending slot')
                    else:
                        # print(f'{start_time_hours}:{start_time_minutes}-{end_time_hours}:{end_time_minutes}')
                        timeSlot = TimeSlot.objects.filter(Q(start_time_hours=start_time_hours) & Q(start_time_minutes=start_time_minutes)).first()
                        print(timeSlot)
                        # making the Board object
                        board_user = request.user
                        time_sched = TimeSchedule.objects.get(time_slot=timeSlot,day=selected_day)
                        print(time_sched)
                        boardObj = Board.objects.get(board_no=board,day=selected_day,time_slot=timeSlot,time_sched=time_sched)
                        print(boardObj)
                        boardObj.board_user = board_user
                        boardObj.save()
                        messages.success(request,f'Slot booked for {request.user.username} for {selected_day} at {start_time_hours}:{start_time_minutes}-{end_time_hours}:{end_time_minutes}')
                        return redirect('profile')
            
            else:
                messages.error(request,f'Failure to book slot. Please try again.')
    
    # getting the remaining time slots for the day
    ist = pytz.timezone('Asia/Kolkata')
    datetime_now = datetime.now(ist)
    curr_time = datetime_now.strftime('%H:%M')
    curr_time_hours,curr_time_minutes = tuple(curr_time.split(':'))
    
    crit = (Q(end_time_hours__gt=curr_time_hours) | (Q(end_time_hours=curr_time_hours) & Q(end_time_minutes__gt=curr_time_minutes)))
    timeslots = TimeSlot.objects.filter(crit).all()
    timescheds = TimeSchedule.objects.filter(day=selected_day).filter(time_slot__in = timeslots).all()
    timescheds = list(timescheds)
    timescheds.sort(key=lambda x: x.time_slot.start_time_hours+x.time_slot.start_time_minutes, reverse=False)
    
    data = {
        'selected_day' : selected_day,
        'days': days,
        'time_schedules': timescheds,
        'boards': Board.objects.filter(day=selected_day).all() 
    }    
    return render(request,'slots/booking.html',context = data)
