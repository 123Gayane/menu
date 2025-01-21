from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, Ingredient


class UserForm1(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "first_name", "last_name"]


class UserForm(forms.ModelForm):
    user_type = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'user_type']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'ingredients']


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'cost']
