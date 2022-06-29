from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.db.models import Q
from slots.models import Board,IPAddress,TimeSlot,TimeSchedule
from .models import Course,Lab
from django.utils import timezone
from datetime import date, timedelta, datetime
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

    # getting available time slots and days
    crit = (Q(end_time_hours__gt=curr_time_hours) | (Q(end_time_hours=curr_time_hours) & Q(end_time_minutes__gt=curr_time_minutes)))
    timeslots = TimeSlot.objects.filter(crit).all()

    # getting the remaining booked slots for today
    booked_slots = Board.objects.filter(board_user=request.user).filter(course=course).filter(day=today).filter(time_slot__in=timeslots).all()
    booked_slots = list(booked_slots)
    # getting the booked time slots for the remaining days of the lab week
    if curr_day != 6:
        days = DAYS_OF_WEEK[curr_day+1:]
        booked_slots += list(Board.objects.filter(board_user=request.user).filter(course=course).filter(day__in=days).all())
    # sorting the booked slots
    booked_slots.sort(key=lambda x: str(day_dict[x.day]+1)+x.time_slot.start_time_hours+x.time_slot.start_time_minutes, reverse=False)


    data = {
        'id':course_id,
        'name':course.name,
        'professors':course.professors.all(),
        'staff':course.staff.all(),
        'description':course.description,
        'labs':Lab.objects.filter(course=course).all(),
        'pending_slots':booked_slots
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


@login_required
def courseInfo(request,course_id):
    course = Course.objects.get(id=course_id)
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
    curr_time_hours, curr_time_minutes = tuple(curr_time.split(':'))
    curr_day = datetime.today().weekday()
    today = DAYS_OF_WEEK[curr_day]

    # getting available time slots and days
    crit = (Q(end_time_hours__gt=curr_time_hours) | (
        Q(end_time_hours=curr_time_hours) & Q(end_time_minutes__gt=curr_time_minutes)))
    timeslots = TimeSlot.objects.filter(crit).all()

    # getting the remaining booked slots for today
    booked_slots = Board.objects.filter(board_user=request.user).filter(
        course=course).filter(day=today).filter(time_slot__in=timeslots).all()
    booked_slots = list(booked_slots)
    # getting the booked time slots for the remaining days of the lab week
    if curr_day != 6:
        days = DAYS_OF_WEEK[curr_day+1:]
        booked_slots += list(Board.objects.filter(board_user=request.user).filter(
            course=course).filter(day__in=days).all())
    # sorting the booked slots
    booked_slots.sort(key=lambda x: str(
        day_dict[x.day]+1)+x.time_slot.start_time_hours+x.time_slot.start_time_minutes, reverse=False)

    data = {
        'id': course_id,
        'name': course.name,
        'professors': course.professors.all(),
        'staff': course.staff.all(),
        'description': course.description,
        'labs': Lab.objects.filter(course=course).all(),
        'pending_slots': booked_slots
    }

    return render(request, 'courses/courseInfo.html', context=data)


@login_required
def deleteLab(request, lab_id, course_id):
    print('ok')
    # fetching and deleting the object
    lab = Lab.objects.get(id=lab_id)
    lab.delete()
    return redirect("courseInfo", course_id=course_id)


@login_required
def updateCourseDes(request, course_id):
    if request.method == 'POST':
        frmCourseDes = request.POST.get('courseDes')
        Course.objects.filter(id=course_id).update(description=frmCourseDes)
    return redirect("courseInfo", course_id=course_id)


@login_required
def updateLabDes(request, course_id, lab_id):
    lab = Lab.objects.get(id=lab_id)
    if request.method == 'POST':
        frmLabName = request.POST.get('labName')
        frmLabDes = request.POST.get('labDes')
        Lab.objects.filter(id=lab_id).update(
            lab_name=frmLabName, description=frmLabDes)
        return redirect("courseInfo", course_id=course_id)
    context = {
        'name': lab.lab_name,
        'description': lab.description,
        'courseID': course_id,
        'labID': lab_id
    }
    return render(request, 'courses/updateLab.html',context=context)

@login_required
def createLab(request, course_id):
    course = Course.objects.get(id=course_id)
    if request.method=='POST':
        lab = Lab(
            lab_no=request.POST.get('labNo'),
            lab_name=request.POST.get('labName'),
            date_due=request.POST.get('labDueDate') +
            ' ' + request.POST.get('labDueTime'),
            description=request.POST.get('labDes'),
            course=course,
            tutorials=request.POST.get('labtut')
        )
        lab.save()
        return redirect("courseInfo", course_id=course_id)
    dt = datetime.now()
    context = {
        'date': dt.strftime("%Y") + '-' + dt.strftime("%m") + '-' + dt.strftime("%d"),
        'time': dt.strftime("%X"),
        'courseID': course_id
    }
    return render(request, 'courses/createLab.html', context=context)