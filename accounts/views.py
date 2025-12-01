from django.shortcuts import render, redirect, HttpResponse
from .models import CustomUser
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password

def home(request):
    return render(request, 'home.html') 

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == "POST":
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        confirm_password = request.POST.get('confirm_password', None)
        if not username or not email or not password:
            return render(request, 'register.html', context={
                'username': username,
                'email': email,
                'error': 'All fields are required'
            })
        if password != confirm_password:
            return render(request, 'register.html', context={
                'username': username,
                'email': email,
                'error': 'Passwords do not match' 
            })
        hash_password = make_password(password)

        user = CustomUser.objects.create_user(email=email, password=hash_password, username=username)
        user.save()
        return redirect('login')            

def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html') 
    elif request.method == 'POST':
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        if not email or not password:
            return render(request, 'login.html', context={
                "email": email,
                "error":"Email must be set"
            })
        user = authenticate(request, email=email, password=password) 
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})   
        
def logout_view(request):
    logout(request)
    return redirect('login')
