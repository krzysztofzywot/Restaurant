from django.db import models
from django.contrib.auth.models import User


class Address(models.Model):
    street = models.CharField(max_length=150)
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=60)
    zip = models.IntegerField()
    country = models.CharField(max_length=60)


    def __str__(self):
        return f"{self.street} {self.city} {self.zip} {self.state} {self.country}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, blank=True, null=True, on_delete=models.SET_NULL)


    def __str__(self):
        return f"{self.user.username}"
