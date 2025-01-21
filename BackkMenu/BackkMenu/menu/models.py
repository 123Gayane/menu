from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('manager', 'Manager'),
        ('chef', 'Chef'),
        ('admin', 'Admin'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return f"{self.user.username} ({self.user_type})"


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('APP', 'Appetizer'),
        ('ENT', 'Entree'),
        ('DES', 'Dessert'),
    ]

    name = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    category = models.CharField(max_length=3, choices=CATEGORY_CHOICES)
    ingredients = models.ManyToManyField(Ingredient)
    description = models.TextField(blank=True, null=True)
    available = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Automatically calculate selling_price as cost + 15%
        if not self.selling_price:
            self.selling_price = self.cost * 1.15
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductIngredient(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.ingredient.name}"

