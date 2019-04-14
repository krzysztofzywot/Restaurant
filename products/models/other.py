from django.db import models


class ItemsWithVariousSize(models.Model):
    """Abstract class that's used as a base for products that may be bought in different sizes."""

    name = models.CharField(max_length=50)
    # Price can be blank if product is not available in specific size.
    price_small = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=11)
    price_large = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=11)


    def __str__(self):
        return self.name


class Sub(ItemsWithVariousSize):
    pass


class DinnerPlatter(ItemsWithVariousSize):
    pass

#########################################################

class ItemsWithUniformSize(models.Model):
    """Abstract class that's used as a base for products that may be bought in only one size."""

    name = models.CharField(max_length=50)
    price = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=11)


    def __str__(self):
        return self.name


class Pasta(ItemsWithUniformSize):
    pass


class Salad(ItemsWithUniformSize):
    pass
