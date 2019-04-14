from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("post/<int:id>", views.display_post, name="display_post")
]
