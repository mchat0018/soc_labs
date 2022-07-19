from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.db.models import Q
from .models import IPAddress, TimeConfig, TimeSchedule, Board, TimeSlot, StartDay
from courses.models import Course
from django.utils import timezone
from datetime import date, timedelta, datetime
import pytz

DAYS_OF_WEEK = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

def ret_lab_days(offset):
    day_list = []

    for i in range(7):
        day_list.append(DAYS_OF_WEEK[(i + offset) % 7])
    
    return day_list

@login_required
def bookSlots(request,course_id):
    course = Course.objects.get(id=course_id)
    # check if user is registered in the course
    if not request.user.profile.staff_cred:
        if request.user not in course.students.all():
            raise PermissionDenied
    else:
        if request.user not in course.professors.all() and request.user not in course.staff.all():
            raise PermissionDenied

    # making a list of all days left in the lab week and finding the current day
    date_now = date.today()
    day_now = date_now.weekday()
    today = DAYS_OF_WEEK[day_now]
    
    # setting an ordered list of the remaining lab days
    days = []
    offset = StartDay.objects.filter(course=course).first().day
    lab_days = ret_lab_days(offset)
    i = day_now - offset
    if i < 0: i += 7

    while i<7:
        days.append(lab_days[i])
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
            
            # checking in case no value was submitted
            if time_slot == '' or board == '': 
                messages.error(request,f'Please select a slot')
                print('No slot selected')           
            
            elif time_slot is not None and board is not None or time_slot:
                # checking if slot limit for the day has been reached
                slot_limit = TimeConfig.objects.filter(course=course).filter(day=selected_day).first().slot_limit
                slots_booked = len(Board.objects.filter(board_user=request.user).filter(course=course).filter(day=selected_day).all())
                
                print(f'{slots_booked}/{slot_limit} slots_booked for {selected_day}')
                
                if(slot_limit<=slots_booked): 
                    messages.error(request,f'Failure to book slot. Slot limit for the day already been reached')
                    print('Failure to book slot. Slot limit for the day already been reached')
                else:
                    # retrieving the TimeSlot object
                    start_time,end_time = tuple(time_slot.replace(' ','').split('-'))
                    start_time_hours,start_time_minutes = tuple(start_time.split(':'))
                    end_time_hours,end_time_minutes = tuple(end_time.split(':'))
                    
                    # getting the current time
                    datetime_now = datetime.now(pytz.timezone('Asia/Kolkata'))
                    curr_time = datetime_now.strftime('%H:%M')
                    # if the time slot booked is a previous time slot, it shouldn't be able to book
                    if(curr_time>=end_time and selected_day==today): 
                        messages.error(request,f'Failure to book slot. Please book a pending slot')
                        print('Failure to book slot. Please book a pending slot')
                    else:
                        # extracting the corresponding time slots
                        time_configs = TimeConfig.objects.filter(course=course).filter(day=selected_day).all()
                        timeSlot = TimeSlot.objects.filter(
                            Q(start_time_hours=start_time_hours) & Q(start_time_minutes=start_time_minutes) 
                            & Q(end_time_hours=end_time_hours) & Q(end_time_minutes=end_time_minutes)
                        ).filter(time_config__in=time_configs).first()
                        # Since there is only one time slot of queried timings that points to a TimeConfig of a particular day
                        # and course  
                        print(timeSlot)
                        # making the Board object
                        board_user = request.user
                        # time_sched = TimeSchedule.objects.get(course=course,day=selected_day,time_slot__in=timeSlots)
                        # print(time_sched)
                        boardObj = Board.objects.get(board_name=board,day=selected_day,time_slot=timeSlot,course=course)
                        print(boardObj)
                        boardObj.board_user = board_user
                        boardObj.save()
                        messages.success(request,f'Slot booked for {request.user.username} for {selected_day} at {start_time_hours}:{start_time_minutes}-{end_time_hours}:{end_time_minutes}')
                        return redirect('course-page',course_id=course_id)
            
            else:
                messages.error(request,f'Failure to book slot. Please try again.')
                print('Failure to book slot. Please try again.')
    
    # getting the remaining time slots for the day
    ist = pytz.timezone('Asia/Kolkata')
    datetime_now = datetime.now(ist)
    curr_time = datetime_now.strftime('%H:%M')
    curr_time_hours,curr_time_minutes = tuple(curr_time.split(':'))
    
    crit = (Q(end_time_hours__gt=curr_time_hours) | (Q(end_time_hours=curr_time_hours) & Q(end_time_minutes__gt=curr_time_minutes)))
    timeslots = TimeSlot.objects.filter(crit).all()
    
    if selected_day==today:
        timescheds = TimeSchedule.objects.filter(course=course).filter(day=selected_day).filter(time_slot__in = timeslots).all()
    else: timescheds = TimeSchedule.objects.filter(course=course).filter(day=selected_day)
    
    timescheds = list(timescheds)
    timescheds.sort(key=lambda x: x.time_slot.start_time_hours+x.time_slot.start_time_minutes, reverse=False)
    
    # We want to order the Board objects (slots) according to the ordering of the IPAddress objects
    
    # Fetching the assigned boards (IPAddress objects)
    boards = IPAddress.objects.filter(course=course).all()
    boards = list(boards)
    # making a dictionary of board names with their indices
    board_dict = {}
    for i in range(len(boards)):
        board_dict[boards[i].board_name] = i
    # ordering the slots accordingly
    slots = list(Board.objects.filter(course=course).filter(day=selected_day).all())
    slots.sort(
        key=lambda x: x.time_slot.start_time_hours+x.time_slot.start_time_minutes+str(board_dict[x.board_name]), 
        reverse=False
    )

    data = {
        'selected_day' : selected_day,
        'days': days,
        'time_schedules': timescheds,
        'boards': slots,
        'IPs': boards
    }    

    # print(Board.objects.filter(course=course).filter(day=selected_day).all())
    return render(request,'slots/booking2.html',context = data)
