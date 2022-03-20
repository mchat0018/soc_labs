from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Profile
from .forms import UserRegisterForm,UserUpdateForm,ProfileForm

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