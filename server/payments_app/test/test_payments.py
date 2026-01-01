from rest_framework.test import APITestCase
from django.urls import reverse
from unittest.mock import patch

from user_app.models import MyUsers
from ticket_app.models import TicketTemplate
from ..models import Order, OrderItem, Payment


class CheckoutTests(APITestCase):
    def setUp(self):
        self.user = MyUsers.objects.create_user(
            username="testuser",
            email="test@test.com",
            password="password123"
        )
        self.client.force_authenticate(self.user)

        self.url = reverse("create_payment_intent")

    @patch("payments_app.views.stripe.PaymentIntent.create")
    def test_checkout_creates_order_and_decrements_inventory(self, mock_stripe):
        mock_stripe.return_value.client_secret = "test_secret"
        mock_stripe.return_value.id = "pi_test"

        tt = TicketTemplate.objects.create(
            title="general",
            available_quantity=5,
            price=100
        )

        payload = {
            "items": [
                {"ticket_template_id": tt.id, "quantity": 2}
            ]
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, 201)

        tt.refresh_from_db()
        self.assertEqual(tt.available_quantity, 3)

        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)
        self.assertEqual(Payment.objects.count(), 1)

        order = Order.objects.first()
        item = order.items.first()

        self.assertEqual(item.quantity, 2)
        self.assertEqual(item.line_total, 200)

    @patch("payments_app.views.stripe.PaymentIntent.create")
    def test_checkout_rolls_back_on_insufficient_inventory(self, mock_stripe):
        mock_stripe.return_value.client_secret = "test_secret"
        mock_stripe.return_value.id = "pi_test"

        tt = TicketTemplate.objects.create(
            title="general",
            available_quantity=1,
            price=100
        )

        payload = {
            "items": [
                {"ticket_template_id": tt.id, "quantity": 2}
            ]
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, 400)

        tt.refresh_from_db()
        self.assertEqual(tt.available_quantity, 1)

        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(OrderItem.objects.count(), 0)
        self.assertEqual(Payment.objects.count(), 0)

    @patch("payments_app.views.stripe.PaymentIntent.create")
    def test_community_lodging_consumes_general(self, mock_stripe):
        mock_stripe.return_value.client_secret = "test_secret"
        mock_stripe.return_value.id = "pi_test"

        general = TicketTemplate.objects.create(
            title="general",
            available_quantity=5,
            price=100
        )
        lodging = TicketTemplate.objects.create(
            title="community lodging",
            available_quantity=3,
            price=150
        )

        payload = {
            "items": [
                {"ticket_template_id": lodging.id, "quantity": 2}
            ]
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, 201)

        general.refresh_from_db()
        lodging.refresh_from_db()

        self.assertEqual(general.available_quantity, 3)
        self.assertEqual(lodging.available_quantity, 1)

    @patch("payments_app.views.stripe.PaymentIntent.create")
    def test_multi_item_cart(self, mock_stripe):
        mock_stripe.return_value.client_secret = "test_secret"
        mock_stripe.return_value.id = "pi_test"

        general = TicketTemplate.objects.create(
            title="general",
            available_quantity=10,
            price=100
        )
        vip = TicketTemplate.objects.create(
            title="vip",
            available_quantity=5,
            price=200
        )

        payload = {
            "items": [
                {"ticket_template_id": general.id, "quantity": 2},
                {"ticket_template_id": vip.id, "quantity": 1},
            ]
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, 201)

        order = Order.objects.first()
        self.assertEqual(order.items.count(), 2)
        self.assertEqual(order.total, 400)
