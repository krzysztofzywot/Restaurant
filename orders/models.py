from django.db import models
from django.conf import settings

from products.models import Topping


class Pizza(models.Model):
    SMALL = 'S'
    LARGE = 'L'
    SIZE_CHOICES = (
        (SMALL, "Small"),
        (LARGE, "Large")
    )

    type = models.CharField(max_length=50)
    size = models.CharField(max_length=1, choices=SIZE_CHOICES)
    toppings_number = models.IntegerField(default=0)
    toppings = models.ManyToManyField(Topping, blank=True, related_name="toppings")
    price = models.DecimalField(default=0.0, decimal_places=2, max_digits=6)


    def __str__(self):
        count = "topping" if self.toppings_number == 1 else "toppings"
        return f"{self.size} {self.type} pizza with {self.toppings_number} {count}"


class OtherProducts(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(default=0.0, decimal_places=2, max_digits=6)


    def __str__(self):
        return self.name


class Sub(OtherProducts):

    def __str__(self):
        return f"{self.name} sub"


class DinnerPlatter(OtherProducts):
    pass


class Salad(OtherProducts):
    pass


class Pasta(OtherProducts):
    pass


class Order(models.Model):
    PENDING = 'P'
    IN_DELIVERY = 'D'
    COMPLETED = 'C'
    ORDER_STATUS_CHOICES = (
        (PENDING, "Pending"),
        (IN_DELIVERY, "In Delivery"),
        (COMPLETED, "Completed")
    )

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)
    pizzas = models.ManyToManyField(Pizza, blank=True, related_name="order")
    subs = models.ManyToManyField(Sub, blank=True, related_name="order")
    pastas = models.ManyToManyField(Pasta, blank=True, related_name="order")
    salads = models.ManyToManyField(Salad, blank=True, related_name="order")
    dinner_platters = models.ManyToManyField(DinnerPlatter, blank=True, related_name="order")
    total_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=6)
    order_status = models.CharField(max_length=1, choices=ORDER_STATUS_CHOICES, default=PENDING)


    def __str__(self):
        return f"Order no {self.id} by {self.customer}"
