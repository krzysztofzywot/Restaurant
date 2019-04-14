from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


from .models import Pizza, Sub, Pasta, Salad, DinnerPlatter, Order
from products.models import Pizza as PizzaProduct

import json

class OrdersTestCase(TestCase):

    def setUp(self):
        self.credentials = {"username": "Test", "password": "testing123"}
        registered_user = User.objects.create_user(**self.credentials)
        self.client.login(**self.credentials)

        pizza_product = PizzaProduct.objects.create(
            type="Regular",
            description="Some description here.",
            price_small_with_cheese=1.0,
            price_small_with_one_topping=2.0,
            price_small_with_two_toppings=3.0,
            price_small_with_three_toppings=4.0,
            price_large_with_cheese=5.0,
            price_large_with_one_topping=6.0,
            price_large_with_two_toppings=7.0,
            price_large_with_three_toppings=8.0
        )

        pizza = Pizza.objects.create(type=pizza_product.type, size="Small", toppings_number=0, price=pizza_product.price_small_with_cheese)

        # Create a test order
        order = Order.objects.create(
            customer = registered_user,
            total_price = pizza.price,
            order_status = Order.PENDING
        )
        order.pizzas.add(pizza)


    def test_process_order_valid(self):
        pizza_product = PizzaProduct.objects.get(pk=1)
        pizza_order = [{
            "itemType": "pizza",
            "itemSize": "Small",
            "itemName": "cheese",
            "itemPrice": str(pizza_product.price_small_with_cheese),
            "itemId": str(pizza_product.id)
        }]

        response = self.client.post(
            reverse("process_order"),
            data=json.dumps(pizza_order),
            content_type="application/json",
            follow=True,
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )

        self.assertEquals(response.status_code, 200)
        self.assertRedirects(response, "/orders/checkout/2")


    def test_process_order_invalid_item_id(self):
        pizza_product = PizzaProduct.objects.get(pk=1)
        pizza_order = [{
            "itemType": "pizza",
            "itemSize": "Small",
            "itemName": "cheese",
            "itemPrice": str(pizza_product.price_small_with_cheese),
            "itemId": "14"
        }]

        response = self.client.post(
            reverse("process_order"),
            data=json.dumps(pizza_order),
            content_type="application/json",
            follow=True,
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )

        self.assertEquals(response.status_code, 400)


    def test_process_order_string_as_item_id(self):
        pizza_product = PizzaProduct.objects.get(pk=1)
        pizza_order = [{
            "itemType": "pizza",
            "itemSize": "Small",
            "itemName": "cheese",
            "itemPrice": str(pizza_product.price_small_with_cheese),
            "itemId": "qwerty12"
        }]

        response = self.client.post(
            reverse("process_order"),
            data=json.dumps(pizza_order),
            content_type="application/json",
            follow=True,
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )

        self.assertEquals(response.status_code, 400)


    def test_process_order_empty_values(self):
        pizza_product = PizzaProduct.objects.get(pk=1)
        pizza_order = [{
            "itemType": "",
            "itemSize": "",
            "itemName": "",
            "itemPrice": "",
            "itemId": ""
        }]

        response = self.client.post(
            reverse("process_order"),
            data=json.dumps(pizza_order),
            content_type="application/json",
            follow=True,
            HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )

        self.assertEquals(response.status_code, 400)


    def test_process_order_get_request(self):
        response = self.client.get(reverse("process_order"))

        self.assertEquals(response.status_code, 403)


    def test_checkout_valid(self):
        order = Order.objects.get(pk=1)

        response = self.client.get(reverse("checkout", args=(order.id,)))

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context["pizzas"].count(), 1)
        self.assertEquals(response.context["total_price"], order.total_price)


    def test_checkout_invalid_order_id(self):
        response = self.client.get(reverse("checkout", args=(2,)))

        self.assertEquals(response.status_code, 404)


    def test_checkout_view_other_users_order(self):
        """Try to view order that has been created by another user"""
        order = Order.objects.get(pk=1)
        response = self.client.get(reverse("checkout", args=(order.id,)))

        # Log in as another user
        self.credentials = {"username": "Test2", "password": "testing123"}
        User.objects.create_user(**self.credentials)
        self.client.login(**self.credentials)

        response = self.client.get(reverse("checkout", args=(order.id,)))

        self.assertEquals(response.status_code, 403)

    def test_checkout_order_not_pending(self):
        """Try to access completed order"""
        order = Order.objects.get(pk=1)
        order.order_status = Order.COMPLETED
        order.save()

        response = self.client.get(reverse("checkout", args=(order.id,)))

        self.assertEquals(response.status_code, 403)


    def test_checkout_anonymous_user(self):
        anonymous_client = Client()

        response = anonymous_client.get(reverse("checkout", args=(1,)))

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, "/login/?next=/orders/checkout/1")
