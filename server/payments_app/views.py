from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as s
import stripe
from .models import Order, OrderItem, Payment
from .serializers import PaymentSerializer
from ticket_app.models import Ticket, TicketTemplate
from falcon_proj import settings
from decimal import Decimal
from django.shortcuts import get_object_or_404
from rest_framework.status import HTTP_400_BAD_REQUEST
from django.db import transaction
from rest_framework.validators import ValidationError


# Create your views here.

stripe.api_key = settings.STRIPE_API_KEY

class CreatePaymentIntent(APIView):
    def post(self, request):
        cart = request.data.get("items")
        if not cart:
            return Response({"detail": "Cart empty"}, status=HTTP_400_BAD_REQUEST)
        with transaction.atomic():
            order = Order.objects.create(user=request.user)
            for item in cart:
                tt = TicketTemplate.objects.select_for_update().get(
                    id=item["ticket_template_id"]
                )

                if item["quantity"] > tt.available_quantity:
                    raise ValidationError("Not enough tickets available.")
                
                tt.available_quantity -= item["quantity"]
                # Recall: community lodging is an upgrade of the general ticket; thus, we need to also reduce the availability of general tickets 
                if tt.title == "community lodging":
                    general = TicketTemplate.objects.select_for_update().get(title="general")
                    if item["quantity"] > general.available_quantity:
                        raise ValidationError(
                            "Not enough general tickets available for community lodging."
                        )
                    general.available_quantity -= item["quantity"]
                    general.save()
                tt.save()
                OrderItem.objects.create(
                    order=order,
                    ticket_template=tt,
                    quantity=item["quantity"],
                    title_at_purchase=tt.title, 
                    unit_price_at_purchase=tt.price,
                    line_total=tt.price*item["quantity"],
                )
            order.recalculate_totals()
            order.save()
            intent = stripe.PaymentIntent.create(
                amount=int(order.total * 100),
                currency="usd",
                metadata={"order_id": order.id},
            )
            Payment.objects.create(
                order=order,
                stripe_payment_intent_id=intent.id,
                status="pending"
            )
        return Response(
            {
                "client_secret": intent.client_secret,
                "order_id": order.id,
            },
            status=201
        )

            
class ViewPayment(APIView):
    def get(self, request):
        staff = getattr(request.user, "is_staff")
        if not staff:
            return Response({'detail': "Only staff can access this."}, status=s.HTTP_403_FORBIDDEN)
        payments = Payment.objects.all(
            status="paid"
        )
        ser_payment = PaymentSerializer(payments, many=True)
        return Response(ser_payment.data, status=s.HTTP_200_OK)