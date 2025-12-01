from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('confirm-code/<int:user_id>/', confirm_code, name='confirm_code'),
    path('profile/', profile, name='profile'),
    path('profile/view/', profile_view, name='profile_view'),
]
