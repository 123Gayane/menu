import profile
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
# from .models import Product, Ingredient, ProductIngredient
from .serializers import *



@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# {
#     "username": "lili",
#     "email": "lil@gmail.com",
#     "password": "ll123ll",
#     "profile": {"user_type": "chef"}
# }

@api_view(['POST'])
def signin(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({'message': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)

    if not user:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    token, created = Token.objects.get_or_create(user=user)

    return Response({'token': token.key}, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_product(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def put_product(request, pk):
    if request.user.profile.user_type == 'chef':
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "Only chefs can update products."}, status=status.HTTP_403_FORBIDDEN)



@api_view(['DELETE'])
def delete_product(request, pk):
    if request.user.profile.user_type == 'manager':
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({"error": "Only managers can delete products."}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def add_ingredient(request):
    if hasattr(request.user, 'profile') and request.user.profile.user_type == 'manager':
        serializer = IngredientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "Only manager can add ingredients."}, status=status.HTTP_403_FORBIDDEN)



@api_view(['DELETE'])
def delete_ingredient(request, pk):
    if hasattr(request.user, 'profile') and request.user.profile.user_type == 'manager':
        try:
            ingredient = Ingredient.objects.get(pk=pk)
        except Ingredient.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        ingredient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({"error": "Only managers can delete ingredients."}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
def get_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_ingredients(request):
    ingredients = Ingredient.objects.all()
    serializer = IngredientSerializer(ingredients, many=True)
    return Response(serializer.data)



@api_view(['PATCH'])
def mark_product_unavailable(request, pk):
        try:
            # Retrieve the product
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            # Return 404 if the product does not exist
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        product.available = not product.available
        product.save()

        # Serialize the updated product
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def log_out(request):
    try:
        logout(request)
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



@api_view(["GET"])
def get_user(request):
    try:
        user = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(user)
        return Response({"user": serializer.data}, status=status.HTTP_200_OK)
    except Profile.DoesNotExist:
        return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)


