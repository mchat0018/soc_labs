from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.db.models import Q
from slots.models import Board,IPAddress,TimeSlot,TimeSchedule,StartDay
from .models import Course,Lab, Tutorial
from django.utils import timezone
from datetime import date, timedelta, datetime
import pytz

DAYS_OF_WEEK = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']


def ret_lab_days(offset):
    day_list = []

    for i in range(7):
        day_list.append(DAYS_OF_WEEK[(i + offset) % 7])
    
    return day_list

def ret_lab_dict(lab_days):
    day_dict = {}

    for i in range(len(lab_days)): day_dict[lab_days[i]] = i
    return day_dict

@login_required
def course_page(request,course_id):
    for c in Course.objects.all(): print(str(c.id))
    course = Course.objects.get(id=course_id)
    print(course)
    # running authentication
    if not request.user.profile.staff_cred:
        if request.user not in course.students.all():
            raise PermissionDenied
    else:
        if request.user not in course.professors.all() and request.user not in course.staff.all():
            raise PermissionDenied
    
    # getting current day and time
    ist = pytz.timezone('Asia/Kolkata')
    datetime_now = datetime.now(ist)
    curr_time = datetime_now.strftime('%H:%M')
    curr_time_hours,curr_time_minutes = tuple(curr_time.split(':'))
    curr_day = datetime.today().weekday()
    today = DAYS_OF_WEEK[curr_day]
    print(curr_time)
    print(today)
    # getting available time slots and days
    crit = (Q(end_time_hours__gt=curr_time_hours) | (Q(end_time_hours=curr_time_hours) & Q(end_time_minutes__gt=curr_time_minutes)))
    timeslots = TimeSlot.objects.filter(crit).all()

    # getting the remaining booked slots for today
    booked_slots = Board.objects.filter(board_user=request.user).filter(course=course).filter(day=today).filter(time_slot__in=timeslots).all()
    booked_slots = list(booked_slots)
    
    # getting the booked time slots for the remaining days of the lab week
    offset = StartDay.objects.filter(course=course).first().day
    lab_days = ret_lab_days(offset)
    curr_day -= offset
    if curr_day < 0: curr_day += 7
    days = []
    if curr_day != 6:
        days = lab_days[curr_day+1:]
        booked_slots += list(Board.objects.filter(board_user=request.user).filter(course=course).filter(day__in=days).all())
    
    print(days)
    # sorting the booked slots
    day_dict = ret_lab_dict(lab_days)
    booked_slots.sort(key=lambda x: str(day_dict[x.day]+1)+x.time_slot.start_time_hours+x.time_slot.start_time_minutes, reverse=False)
    
    print(booked_slots)
    print(lab_days[curr_day])

    data = {
        'id':course_id,
        'name':course.name,
        'professors':course.professors.all(),
        'staff':course.staff.all(),
        'description':course.description,
        'tutorials':Tutorial.objects.filter(course=course).all(),
        'pending_slots':booked_slots,
        'curr_day':today,
        'curr_time_hours': curr_time_hours,
        'curr_time_minutes': curr_time_minutes
    }

    return render(request,'courses/course_page.html',context=data)

def lab_page(request,course_id,lab_no):
    course = Course.objects.get(pk=course_id)
    lab = Lab.objects.get(course=course,lab_no=lab_no)
    # running authentication
    if not request.user.profile.staff_cred:
        if request.user not in course.students.all():
            raise PermissionDenied
    else:
        if request.user not in course.professors.all() and request.user not in course.staff.all():
            raise PermissionDenied

    data = {
        'lab_no':lab.lab_no,
        'lab_name':lab.lab_name,
        'date_created':lab.date_created,
        'date_due':lab.date_due,
        'description':lab.description,
        'tutorials':lab.tutorials,
        'course':course
    }

    return render(request,'courses/lab_page.html',context=data)