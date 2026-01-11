import stripe
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from falcon_proj import settings
from .models import Order, Payment
from django.db import transaction
from django.utils import timezone
from .services import release_order_inventory

stripe.api_key = settings.STRIPE_API_KEY

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    # --- Payment succeeded ---
    if event["type"] == "payment_intent.succeeded":
        intent = event["data"]["object"]
        order_id = intent.metadata.get("order_id")

        if not order_id:
            return HttpResponse(status=400)

        # Idempotent updates
        Order.objects.filter(id=order_id).update(status="paid")
        Payment.objects.filter(
            stripe_payment_intent_id=intent.id
        ).update(status="paid")

    # --- Payment failed ---
    elif event["type"] == "payment_intent.payment_failed":
        intent = event["data"]["object"]
        order_id = intent.metadata.get("order_id")

        if order_id:
            Order.objects.filter(id=order_id).update(status="failed")

    return HttpResponse(status=200)
