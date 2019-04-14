from django.urls import path

from . import views

urlpatterns = [
    path("process_order/", views.process_order, name="process_order"),
    path("add_toppings/", views.add_toppings, name="add_toppings"),
    path("checkout/<int:order_id>", views.checkout, name="checkout"),
    path("complete/", views.complete, name="complete"),
    path("my_orders/", views.my_orders, name="my_orders")
]
