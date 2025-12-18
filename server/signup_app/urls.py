from .views import Sign_Up
from django.urls import path

urlpatterns = [
    path('new_account/', Sign_Up.as_view(), name='new_account'),
]