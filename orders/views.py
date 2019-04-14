from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.exceptions import PermissionDenied
import json

from .models import Order, Pizza, Sub, DinnerPlatter, Pasta, Salad
from products.models import Pizza as PizzaProduct, Sub as SubProduct, DinnerPlatter as DinnerPlatterProduct, Pasta as PastaProduct, Salad as SaladProduct
from products.models import Topping
import orders.validations as validations


def process_order(request):
    """
    Function is called by XMLHttpRequest when user wants to make a new order.
    Function checks if sent JSON object contains data and if they are correct, and then it creates an Order object
    and fills it in with items chosen by the user.
    Finally, it redirects to the Checkout function where user can finalize his order.
    """

    if request.method == "POST":
        if not request.body:
            return HttpResponseBadRequest("<h1>No data.</h1>")

        order_JSON = json.loads(request.body)
        order = Order.objects.create()

        total_price = 0

        try:
            for item in order_JSON:
                size = item["itemSize"]

                # Make sure that all the necessary informations about the item are provided
                if not item["itemType"] or not item["itemId"] or not item["itemName"]:
                    return HttpResponseBadRequest("<h1>Missing information about product.</h1>")

                if item["itemType"] == "pizza":
                    pizza_type, no_of_toppings, price = validations.get_pizza(item["itemId"], item["itemName"], size)

                    total_price += price
                    order.pizzas.add(Pizza.objects.create(type=pizza_type, size=size, toppings_number=no_of_toppings, price=price))
                elif item["itemType"] == "sub":
                    name, price = validations.get_sub(item["itemId"], size)

                    total_price += price
                    order.subs.add(Sub.objects.create(name=name, price=price))
                elif item["itemType"] == "pasta":
                    name, price = validations.get_pasta(item["itemId"])

                    total_price += price
                    order.pastas.add(Pasta.objects.create(name=name, price=price))
                elif item["itemType"] == "salad":
                    name, price = validations.get_salad(item["itemId"])

                    total_price += price
                    order.salads.add(Salad.objects.create(name=name, price=price))
                elif item["itemType"] == "dinnerPlatter":
                    name, price = validations.get_dinner_platter(item["itemId"], size)

                    total_price += price
                    order.dinner_platters.add(DinnerPlatter.objects.create(name=name, price=price))
        except validations.NonexistentProduct:
            return HttpResponseBadRequest("<h1>One or more products you selected do not exist.</h1>")
        except ValueError:
            return HttpResponseBadRequest("<h1>Incorrect product information.</h1>")


        order.total_price = total_price
        order.save()

        return HttpResponseRedirect(reverse("checkout", args=(order.id,)))
    else:
        raise PermissionDenied


def add_toppings(request):
    """
    Function is called by XMLHttpRequest when user wants to submit toppings to his pizza.
    It checks whether sent JSON object contains data and whether it is correct, and then it sets the toppings for pizza
    with the selected id.
    """
    if request.method == "POST":
        if not request.POST["pizza_id"] or not request.POST["toppings_ids"]:
            return HttpResponse("No data.")

        pizza_id = request.POST["pizza_id"]
        toppings_ids = json.loads(request.POST["toppings_ids"])

        try:
            pizza = Pizza.objects.get(pk=pizza_id)
            order = pizza.order.first()
        except Pizza.DoesNotExist:
            return JsonResponse({"status": 400})

        # Make sure that user wants to set toppings for his own order.
        if order.customer != request.user:
            raise PermissionDenied
        # Make sure that the number of toppings is equal to the declared toppings_number.
        elif pizza.toppings_number != len(toppings_ids):
            return JsonResponse({"status": 400})

        # Add toppings to the selected pizza.
        for id in toppings_ids:
            pizza.toppings.add(Topping.objects.get(pk=id))

        return JsonResponse({"status": 200})
    else:
        raise PermissionDenied


@login_required
@ensure_csrf_cookie
def checkout(request, order_id):
    """Function allows user to confirm and finalize his order"""
    order = get_object_or_404(Order, pk=order_id)

    # If the selected order already has a customer id set and it's not the same as id of the user that tries to view this order,
    # raise PermissionDenied.
    if order.customer and order.customer != request.user:
        raise PermissionDenied
    # If the selected order is already in delivery or has been completed, user should not be able to display this page.
    elif order.order_status != Order.PENDING:
        raise PermissionDenied

    # Set the customer id for this order to be the id of the user
    order.customer = request.user
    order.save()

    context = {
        "pizzas": order.pizzas.all(),
        "subs": order.subs.all(),
        "pastas": order.pastas.all(),
        "salads": order.salads.all(),
        "dinner_platters": order.dinner_platters.all(),
        "total_price": order.total_price,
        "toppings": Topping.objects.all()
    }

    # Store the order id of this page.
    request.session["order_id"] = order_id

    return render(request, "orders/checkout.html", context)


@login_required
def complete(request):
    """Display an order completion page after the user has successfully placed an order."""

    if request.session["order_id"]:
        order = Order.objects.get(pk=request.session["order_id"])
        pizzas = order.pizzas.all()

        for pizza in pizzas:
            # If the user didn't select appropriate number of toppings, redirect him back to the checkout page
            # and display an error
            if pizza.toppings.count() != pizza.toppings_number:
                messages.add_message(request, messages.ERROR, "You must select an appropriate number of toppings before finishing the order.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        # Once order has been completed, remove the order_id from the session
        request.session["order_id"] = ""
    else:
        raise PermissionDenied

    return render(request, "orders/complete.html")


@login_required
def my_orders(request):
    """Display user orders"""
    orders = Order.objects.filter(customer=request.user).all()

    return render(request, "orders/my_orders.html", {"orders": orders})
