from django.urls import path
from django.conf.urls import include
from . import views


urlpatterns = [
    path('', views.checkout_order, name='checkout'),
    path('paypal/', include('paypal.standard.ipn.urls')),
]
