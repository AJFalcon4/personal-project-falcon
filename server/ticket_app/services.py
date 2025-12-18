import stripe
from dotenv import load_dotenv
load_dotenv()
import os
stripe.api_key = os.getenv("STRIPE_API_KEY")

payment_intent = stripe.PaymentIntent.create(
  amount=2000,
  currency="usd",
  automatic_payment_methods={"enabled": True},
)