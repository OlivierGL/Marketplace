from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='market-home'),
    path('paintings/', views.paintings, name='market-paintings'),
    path('paintings/product/<int:pk>/', views.product, name='product_with_pk'),
    path('paintings/product/<int:pk>/modify/', views.modify_product.as_view(), name="modify_product"),
    path('paintings/product/<int:pk>/delete/', views.delete_product.as_view(), name="delete_product"),

    path('sculptures/', views.sculptures, name='market-sculptures'),
    path('sculptures/product/<int:pk>/', views.product, name='product_with_pk'),
    path('sculptures/product/<int:pk>/modify/', views.modify_product.as_view(), name="modify_product"),
    path('sculptures/product/<int:pk>/delete/', views.delete_product.as_view(), name="delete_product"),

    path('clothes/', views.clothes, name='market-clothes'),
    path('clothes/product/<int:pk>/', views.product, name='product_with_pk'),
    path('clothes/product/<int:pk>/modify/', views.modify_product.as_view(), name="modify_product"),
    path('clothes/product/<int:pk>/delete/', views.delete_product.as_view(), name="delete_product"),

    path('jewelry/', views.jewelry, name='market-jewelry'),
    path('jewelry/product/<int:pk>/', views.product, name='product_with_pk'),
    path('jewelry/product/<int:pk>/modify/', views.modify_product.as_view(), name="modify_product"),
    path('jewelry/product/<int:pk>/delete/', views.delete_product.as_view(), name="delete_product"),

    path('glass_art/', views.glass_art, name='market-glass_art'),
    path('glass_art/product/<int:pk>/', views.product, name='product_with_pk'),
    path('glass_art/product/<int:pk>/modify/', views.modify_product.as_view(), name="modify_product"),
    path('glass_art/product/<int:pk>/delete/', views.delete_product.as_view(), name="delete_product"),

    path('cart/', views.cart, name='cart'),
    path('product/<int:pk>/', views.product, name='product_with_pk'),
    path('product/<int:pk>/modify/', views.modify_product.as_view(), name="modify_product"),
    path('product/<int:pk>/delete/', views.delete_product.as_view(), name="delete_product"),

    path('profile/<int:primary_key>/add_product/', views.add_product.as_view(), name='add_product'),
    path('profile/<int:primary_key>/product/<int:pk>/', views.product_prof, name='product_with_pk'),
    path('profile/<int:primary_key>/product/<int:pk>/modify/', views.modify_product.as_view(), name="modify_product"),
    path('profile/<int:primary_key>/product/<int:pk>/delete/', views.delete_product.as_view(), name="delete_product"),
]
