from django.db import models
from .addons import Topping


class Pizza(models.Model):
    type = models.CharField(max_length=50)
    description = models.TextField()

    # Restaurant owner may set prices for different variations of pizza
    price_small_with_cheese = models.DecimalField(default=0.0, decimal_places=2, max_digits=6)
    price_small_with_one_topping = models.DecimalField(default=0.0, decimal_places=2, max_digits=6)
    price_small_with_two_toppings = models.DecimalField(default=0.0, decimal_places=2, max_digits=6)
    price_small_with_three_toppings = models.DecimalField(default=0.0, decimal_places=2, max_digits=6)

    price_large_with_cheese = models.DecimalField(default=0.0, decimal_places=2, max_digits=6)
    price_large_with_one_topping = models.DecimalField(default=0.0, decimal_places=2, max_digits=6)
    price_large_with_two_toppings = models.DecimalField(default=0.0, decimal_places=2, max_digits=6)
    price_large_with_three_toppings = models.DecimalField(default=0.0, decimal_places=2, max_digits=6)


    def __str__(self):
        return f"{self.type} pizza"
