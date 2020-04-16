from django.urls import path
from django.conf.urls import include
from . import views


urlpatterns = [
    path('checkout/', views.checkout_order, name='checkout'),
    path('review-shipping/', views.shipping_info, name='review-shipping'),
    path('successful-payment/', views.successful_payment, name='successful-payment'),
    path('canceled-payment/', views.canceled_payment, name='canceled-payment'),
    path('orders-history/', views.orders_history, name='orders-history'),
    path('paypal/', include('paypal.standard.ipn.urls')),
]
