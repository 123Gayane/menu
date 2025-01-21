
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('products/', views.get_products, name='product-list'),
    path('products/add/', views.add_product, name='product-add'),
    path('products/<int:pk>/', views.put_product, name='product-update'),
    path('products/<int:pk>/delete/', views.delete_product, name='product-delete'),
    path('ingredients/', views.get_ingredients, name='ingredient-list'),
    path('ingredients/add/', views.add_ingredient, name='ingredient-add'),
    path('ingredients/<int:pk>/delete/', views.delete_ingredient, name='ingredient-delete'),
    path('products/<int:pk>/unavailable/', views.mark_product_unavailable, name='mark_product_unavailable'),
    path('log_out/', views.log_out, name='log_out'),
    path('get_user/', views.get_user, name='get_user')

]