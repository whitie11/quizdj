from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# Create your models here.
class QuizUser(AbstractUser):
    
    ROLE_CHOICE = [('Admin', 'Admin User'),
                   ('StdUser', 'Standard User'), ('Guest', 'Guest')]

    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICE, default='StdUser')