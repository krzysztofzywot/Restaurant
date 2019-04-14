from products.models import Pizza as PizzaProduct, Sub as SubProduct, DinnerPlatter as DinnerPlatterProduct, Pasta as PastaProduct, Salad as SaladProduct
from products.models import Topping

class NonexistentProduct(Exception):
    """Product with specified id does not exist."""
    pass


def get_pizza(pizza_id, pizza_name, pizza_size):
    # Get information about product.
    try:
        product = PizzaProduct.objects.get(pk=pizza_id)
    except PizzaProduct.DoesNotExist:
        raise NonexistentProduct

    pizza_type = product.type
    # Possible pizza_names: cheese, topping1, topping2, topping3.
    no_of_toppings = 0 if pizza_name == "cheese" else int(pizza_name[-1])
    small_prices = {
        0: product.price_small_with_cheese,
        1: product.price_small_with_one_topping,
        2: product.price_small_with_two_toppings,
        3: product.price_small_with_three_toppings
    }
    large_prices = {
        0: product.price_large_with_cheese,
        1: product.price_large_with_one_topping,
        2: product.price_large_with_two_toppings,
        3: product.price_large_with_three_toppings
    }

    price = 0
    if pizza_size == "Small":
        price = small_prices[no_of_toppings]
    elif pizza_size == "Large":
        price = large_prices[no_of_toppings]

    return pizza_type, no_of_toppings, price


def get_sub(sub_id, sub_size):
    try:
        product = SubProduct.objects.get(pk=sub_id)
    except SubProduct.DoesNotExist:
        raise NonexistentProduct

    if sub_size == "Small":
        price = product.price_small
    elif sub_size == "Large":
        price = product.price_large

    return product.name, price


def get_pasta(pasta_id):
    try:
        product = PastaProduct.objects.get(pk=pasta_id)
    except PastaProduct.DoesNotExist:
        raise NonexistentProduct

    return product.name, product.price


def get_salad(salad_id):
    try:
        product = SaladProduct.objects.get(pk=salad_id)
    except SaladProduct.DoesNotExist:
        raise NonexistentProduct

    return product.name, product.price


def get_dinner_platter(dp_id, dp_size):
    try:
        product = DinnerPlatterProduct.objects.get(pk=dp_id)
    except DinnerPlatterProduct.DoesNotExist:
        raise NonexistentProduct

    if dp_size == "Small":
        price = product.price_small
    elif dp_size == "Large":
        price = product.price_large

    return product.name, price
