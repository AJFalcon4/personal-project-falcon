from django.shortcuts import render
from .models import MyUsers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate

from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_204_NO_CONTENT,
)

class Sign_Up(APIView):
    def post(self, request):
        request.data["username"] = request.data["email"]
        users = MyUsers.objects.create_user(**request.data)
        token = Token.objects.create(user=users)
        users.save()
        return Response (
            {'user': users.email, 'token':token.key}, status=HTTP_201_CREATED
        )

class Log_in(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get('password')
        users = authenticate(username=email, password=password)
        if users:
            token, created = Token.objects.get_or_create(user=users)
            return Response({"token": token.key, "users": users.email})
        else:
            return Response("No user matching credentials", status=HTTP_404_NOT_FOUND)
        
class Log_out(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=HTTP_204_NO_CONTENT)
    
class Master_Sign_Up(APIView):

        def post(self, request):
            master_users = MyUsers.objects.create_user(**request.data)
            master_users.is_staff = True
            master_users.is_superuser = True
            master_users.save()
            token = Token.objects.create(user=MyUsers)
            return Response(
                {"master_Users": master_users.email, "token": token.key}, status=HTTP_201_CREATED
            )