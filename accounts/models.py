from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=6, blank=True, null=True)
    code_created_at = models.DateTimeField(blank=True, null=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    
