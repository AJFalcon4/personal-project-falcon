from django.core import serializers
from .models import MyUsers

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUsers
        fields = ['email', 'comments']