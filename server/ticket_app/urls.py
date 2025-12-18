from .views import TicketView
from django.urls import path

urlpatterns = [
    path('purchase/', TicketView.as_view(), name='ticket_purchase'),
]