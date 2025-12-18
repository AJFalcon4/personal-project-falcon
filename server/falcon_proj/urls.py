from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("ticket/", include("ticket_app.urls")),
    path("signup/", include("signup_app.urls"))
]

"""
NEXT TO DO LIST:
Look at Signup App Post Method, Check Arguments
Postman: Build the post request, pass Arguments (email, password)
If that works, Django will send Postman Auth Token
Can copy and save file, may use for other post request
"""
