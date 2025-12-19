from django.db import models
from django.contrib.auth.models import AbstractUser

class MyUsers(AbstractUser):
    # Fields for users
    email = models.EmailField(unique=True)
    comments = models.TextField()
    
    # Information about fields
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
