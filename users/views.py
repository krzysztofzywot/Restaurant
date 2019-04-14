from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import RegistrationForm, AddressForm
from .models import Profile


def register(request):
    """Registration of a new user"""

    # Send the user back to the homepage if he is already logged in.
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            # If submitted data is correct, add new user to the database.
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            # Log the user in after registration.
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("register_success")
    else:
        form = RegistrationForm()

    return render(request, "users/register.html", {"form": form})


def register_success(request):
    """Inform the user about successfull registration."""
    return render(request, "users/registerSuccess.html")


@login_required
def profile(request):
    """User profile"""
    return render(request, "users/profile.html")


@login_required
def add_address(request):
    """Alows the user to add an address."""
    if request.method == "POST":
        form = AddressForm(request.POST)

        if form.is_valid():
            address = form.save()
            # Retrieve the current user's profile and update his address
            user = User.objects.get(username=request.user)
            profile = Profile.objects.get(user=user.id)
            profile.address = address
            profile.save()

            # Redirect the user back to his order if there is order_id stored in session.
            # Otherwise redirect to the main page.
            if request.session["order_id"]:
                return HttpResponseRedirect(reverse("checkout", args=(request.session["order_id"],)))
            else:
                return HttpResponseRedirect(reverse("index"))
    else:
        form = AddressForm()

    return render(request, "users/add_address.html", {"address_form": form})
