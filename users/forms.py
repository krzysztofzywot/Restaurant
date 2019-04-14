from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Address


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")


    # First name and last name fields must be required
    def clean_first_name(self):
        cleaned_data = super().clean()
        first_name = cleaned_data["first_name"]

        if not first_name:
            raise forms.ValidationError("You must enter your first name.", code="no_first_name")

        return first_name


    def clean_last_name(self):
        cleaned_data = super().clean()
        last_name = cleaned_data["last_name"]

        if not last_name:
            raise forms.ValidationError("You must enter your last name.", code="no_last_name")

        return last_name


class AddressForm(forms.ModelForm):

        class Meta:
            model = Address
            fields = ("street", "city", "state", "zip", "country")
