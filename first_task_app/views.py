from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def forget_password(request):
    return render(request, 'forgot-password.html')


def index(request):
    return render(request, 'index.html')


def logoutUser(request):
    logout(request)
    return redirect('login')
