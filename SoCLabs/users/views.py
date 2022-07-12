import smtplib
import re
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Q
import pandas as pd
import secrets
import string

from courses.models import Course
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


def registerCSV(request):
    if request.method == 'POST':
        url = str(request.POST.get('url'))
        url = url.replace('/edit#gid=', '/export?gid=')
        data = pd.read_csv(url + '&format=csv')
        source = string.ascii_letters + string.digits + string.punctuation
        pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
        userLst = []
        for i in data.itertuples():
            username = str(i[1])
            email = str(i[2])
            if not re.match(pat, email):
                continue
            if User.objects.filter(username=username,email=email):
                continue
            password = ''.join((secrets.choice(source) for _ in range(8)))
            User.objects.create(
                username = username,
                email = email,
                password = password
            )
            userLst.append([username, email])
        return render(request, 'users/regUsers.html', {'users': userLst})

    return render(request, 'users/registerCSV.html')


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


def sendPass(request):
    if request.method == 'POST':
        user = User.objects.get(
            username=request.POST.get('username'),email=request.POST.get('email'))
        if user:
            try:
                #Create your SMTP session
                smtp = smtplib.SMTP('smtp.gmail.com', 587)

            #Use TLS to add security
                smtp.starttls()

                #User Authentication
                smtp.login("arpajitofficial@gmail.com", "skcgsgxxtiohpiqm")

                #Defining The Message
                message = '\nReset password here: ' + str(request.get_host()) + '/resetPass/'

                #Sending the Email
                smtp.sendmail("arpajitofficial@gmail.com", str(user.email), message)

                #Terminating the session
                smtp.quit()
                print("Email sent successfully!")

            except Exception as ex:
                print("Something went wrong....", ex)

            return redirect('login')
    return render(request, 'users/sendPass.html')


def resetPass(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(
                username=request.POST.get('username'),email=request.POST.get('email'))
        except:
            return render(request, 'users/resetPass.html')
        if user:
            if request.POST.get('password'):
                user.set_password(request.POST.get('password'))
                user.save()
            return redirect('login')
    return render(request, 'users/resetPass.html')


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