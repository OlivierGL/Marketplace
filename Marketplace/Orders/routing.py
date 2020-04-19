from django.urls import path

from . import consumers

websocket_urlpatterns = [
  path('ws/validateProductsOnStock/', consumers.OrdersConsumer, name='validate_stock'),
]
