from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='market-home'),
    path('paintings/', views.paintings, name='market-paintings'),
    path('sculptures/', views.sculptures, name='market-sculptures'),
    path('clothes/', views.clothes, name='market-clothes'),
    path('jewelry/', views.jewelry, name='market-jewelry'),
    path('glass_art/', views.glass_art, name='market-glass_art'),
    path('cart/', views.cart, name='cart'),
    path('product/<int:primary_key>/', views.product, name='product_with_pk')
]
