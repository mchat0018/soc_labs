from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Q

from courses.models import Course
from .models import Profile
from slots.models import Board,TimeConfig,TimeSchedule,TimeSlot
from .forms import UserRegisterForm,UserUpdateForm,ProfileForm
from datetime import datetime
import time
import pytz

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
    
    reg_courses = request.user.profile.courses.all()
    
    context = {
        'u_form':u_form,
        'p_form':p_form,
        'reg_courses':reg_courses
    }
    return render(request,'users/profile.html',context)


@login_required
def addCourse(request):
    if request.method == 'POST':
        frmCode = request.POST.get('CourseCode')
        # fetching the course
        course = Course.objects.filter(course_code=frmCode).first()
        #  if the code entered was valid and the student isn't already enrolled in the course
        if course is not None and request.user not in course.students.all():
            course.students.add(request.user)
            messages.success(request,f'You have successfully enrolled in {course.name}')
        else: messages.error(request,'Incorrect course code')

    return redirect('profile')