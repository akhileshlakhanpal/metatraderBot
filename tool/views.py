from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import *
from django.shortcuts import get_object_or_404
from django.shortcuts import render

def signin(request):
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/dashboard')
        else:
            messages.error(request, "Please check your Password")
            return render(request, 'pages/login.html')
    else:
        return render(request, 'pages/login.html')

def dashboard(request):
    return render(request,'pages/dashboard.html')

def manage_slave(request):
    return render(request,'pages/manage_slave.html')

def manage_master(request):
    return render(request,'pages/manage_master.html')

def groups_copier(request):
    return render(request,'pages/groups_copier.html')

def servers(request):
    return render(request,'pages/servers.html')