from django.urls import path
from django.conf.urls import include
from . import views


urlpatterns = [
    path('checkout/', views.checkout_order, name='checkout'),
    path('review-shipping/', views.shipping_info, name='review-shipping'),
    path('paypal/', include('paypal.standard.ipn.urls')),
]
