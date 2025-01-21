import re

from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Product, Ingredient, ProductIngredient, Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user_type']


class ProfSerial(serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('id', 'user_type')

    def get_user_type(self, obj):
        return obj.get_user_type_display()

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'profile']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, value):
            raise serializers.ValidationError("Enter a valid email address.")
        return value

    def validate(self, data):
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return data

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        if not Profile.objects.filter(user=user).exists():
            Profile.objects.create(user=user, **profile_data)
        return user

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'cost']


class ProductIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()

    class Meta:
        model = ProductIngredient
        fields = ['id', 'ingredient', 'quantity']


# class ProductSerializer(serializers.ModelSerializer):
#     # ingredients = ProductIngredientSerializer(many=True)
#     cost = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
#     selling_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
#     ingredients = IngredientSerializer(many=True, required=False)

class ProductSerializer(serializers.ModelSerializer):
    ingredient_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )
    ingredients = IngredientSerializer(many=True, read_only=True)  # Nested serializer
    cost = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    selling_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Product
        fields = ['id','name', 'cost', 'category', 'description', 'ingredients','ingredient_ids',  'available', 'selling_price']
        extra_kwargs = {
            'cost': {'required': True},
            'ingredient_ids': {'required': True},
        }

    def validate(self, data):
        if data.get('cost') is None:
            raise serializers.ValidationError({'cost': 'This field is required.'})
        return data

    def create(self, validated_data):
        ingredient_ids = validated_data.pop('ingredient_ids')
        product = Product.objects.create(**validated_data)
        product.ingredients.set(Ingredient.objects.filter(id__in=ingredient_ids))
        product.cost = sum(ingredient.cost for ingredient in product.ingredients.all())
        product.save()
        return product


class ProductSerial(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        product = Product.objects.create(**validated_data)

        # Add ingredients to the product
        for ingredient_data in ingredients_data:
            ingredient, created = Ingredient.objects.get_or_create(**ingredient_data)
            product.ingredients.add(ingredient)

        # Calculate cost and price
        product.cost = sum(ingredient.cost for ingredient in product.ingredients.all())
        product.price = product.cost * 1.15
        product.save()

        return product