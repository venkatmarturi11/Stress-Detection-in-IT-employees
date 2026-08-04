from django.shortcuts import render
from users.forms import UserRegistrationForm
from users.utility.GetImageStressDetection import ImageExpressionDetect


def index(request):
    return render(request, 'index.html', {})

def logout(request):
    return render(request, 'index.html', {})

def UserLogin(request):
    return render(request, 'login.html', {})

def AdminLogin(request):
    return render(request, 'admin-login.html', {})

def UserRegister(request):
    form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})
