from django.http import HttpResponse
from django.shortcuts import render
from .models import Pizza, Sub, DinnerPlatter, Topping, Pasta, Salad

from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def menu(request):
    """Menu z dostępnymi produktami"""

    context = {
        "pizzas": Pizza.objects.all(),
        "toppings": Topping.objects.all(),
        "subs": Sub.objects.all(),
        "pastas": Pasta.objects.all(),
        "salads": Salad.objects.all(),
        "dinnerPlatters": DinnerPlatter.objects.all(),
        "display_shopping_cart": True
    }

    return render(request, "products/menu.html", context)
