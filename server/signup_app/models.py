from django.db import models
from django.contrib.auth.models import AbstractUser

class MyUsers(AbstractUser):
    # Fields for users
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)
    comments = models.TextField()
    
    # Information about fields
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
