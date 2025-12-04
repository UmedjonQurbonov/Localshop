from django.shortcuts import render, redirect, HttpResponse
from .models import CustomUser
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password
from .utils import send_activation_code
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.hashers import check_password


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

        user = CustomUser.objects.create_user( email=email, password=password, username=username, is_active=False )
        user.save()
        send_activation_code(user)
        return redirect('confirm_code', user_id=user.id)            

def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            return render(request, 'login.html', {"email": email, "error": "Email and password are required."})

        user = authenticate(request, email=email, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect('home')
            else:
                print('error active')
                return render(request, 'login.html', {"error": "Account is not activated."})
        else:
            print('error credential')
            return render(request, 'login.html', {"error": "Invalid credentials."})
        
def logout_view(request):
    logout(request)
    return redirect('login')

def confirm_code(request, user_id):
    user = CustomUser.objects.get(pk=user_id)

    if request.method == "POST":
        code = request.POST.get('code')
        if user.activation_code == code:
            if user.code_created_at + timedelta(minutes=10) >= timezone.now():
                user.is_active = True
                user.activation_code = None
                user.code_created_at = None
                user.save()
                return redirect('login')
            else:
                error = "Срок действия кода истёк."
        else:
            error = "Неверный код."
        return render(request, 'confirm_code.html', {'error': error})

    return render(request, 'confirm_code.html')
from django.shortcuts import render, redirect
from .models import UserProfile
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        request.user.username = request.POST.get('username', request.user.username)
        profile.phone = request.POST.get('phone', profile.phone)
        profile.bio = request.POST.get('bio', profile.bio)

        if request.FILES.get('avatar'):
            profile.avatar = request.FILES['avatar']

        request.user.save()
        profile.save()
        return redirect('profile')

    return render(request, 'profile.html', {'user': request.user, 'profile': profile})

@login_required
def profile_view(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    return render(request, 'profile_view.html', {
        'profile': profile,
        'user': request.user
    })
