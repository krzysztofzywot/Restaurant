from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("register/success/", views.register_success, name="register_success"),
    path("profile/", views.profile, name="profile"),
    path("add_address/", views.add_address, name="add_address")
]
