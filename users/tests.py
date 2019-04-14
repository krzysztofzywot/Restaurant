from django.test import TestCase

from .forms import RegistrationForm, AddressForm


class ProfileTestCase(TestCase):

    def test_register_form_valid(self):
        # Test with correct data
        form_data = {
            "username": "Test",
            "email": "test@company.com",
            "first_name": "Test",
            "last_name": "Test",
            "password1": "zaq1@WSX",
            "password2": "zaq1@WSX"
        }

        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())


    def test_register_form_passwords_not_matching(self):
        form_data = {
            "username": "Test2",
            "email": "test2@company.com",
            "first_name": "Test",
            "last_name": "Testing",
            "password1": "test3",
            "password2": "321testing"
        }

        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())


    def test_register_form_two_users_with_same_data(self):
        """Try to create 2 users with the same data"""
        form_data = {
            "username": "Test2",
            "email": "test2@company.com",
            "first_name": "Test",
            "last_name": "Testing",
            "password1": "zaq1@WSX",
            "password2": "zaq1@WSX"
        }

        form = RegistrationForm(data=form_data)
        form.save()

        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())


    def test_register_form_invalid_password_length(self):
        """User with password that contains less than 8 characters"""
        form_data = {
            "username": "Test2",
            "email": "test2@company.com",
            "first_name": "Test",
            "last_name": "Testing",
            "password1": "abcd12",
            "password2": "abcd12"
        }

        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())


    def test_register_form_numeric_password(self):
        """User with entirely numeric password"""
        form_data = {
            "username": "Test2",
            "email": "test2@company.com",
            "first_name": "Test",
            "last_name": "Testing",
            "password1": "623436345",
            "password2": "623436345"
        }

        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())


    def test_register_form_no_first_name(self):
        """User without first name"""
        form_data = {
            "username": "Test2",
            "email": "test2@company.com",
            "first_name": "",
            "last_name": "Testing",
            "password1": "623436345",
            "password2": "623436345"
        }

        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())


    def test_register_form_no_last_name(self):
        """User without first name"""
        form_data = {
            "username": "Test2",
            "email": "test2@company.com",
            "first_name": "Test",
            "last_name": "",
            "password1": "623436345",
            "password2": "623436345"
        }

        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())


    def test_create_address_form_valid(self):
        address = {
            "street": "Street 51",
            "city": "Test City",
            "state": "Test State",
            "zip": "123456",
            "country": "Test Country"
        }
        form = AddressForm(data=address)
        self.assertTrue(form.is_valid())


    def test_create_address_form_invalid(self):
        address = {
            "street": "",
            "city": "Test City",
            "state": "Test State",
            "zip": "Abcdefg",
            "country": "Test Country"
        }
        form = AddressForm(data=address)
        self.assertFalse(form.is_valid())
