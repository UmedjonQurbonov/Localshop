from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.conf import settings

class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=6, blank=True, null=True)
    code_created_at = models.DateTimeField(blank=True, null=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.email
    
