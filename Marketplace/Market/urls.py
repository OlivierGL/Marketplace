from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='market-home'),
    path('paintings/', views.paintings, name='market-paintings'),
    path('sculptures/', views.sculptures, name='market-sculptures'),
    path('clothes/', views.clothes, name='market-clothes'),
    path('jewelry/', views.jewelry, name='market-jewelry'),
    path('glass_art/', views.glass_art, name='market-glass_art'),
]