from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/addProductToCart/', consumers.ProductConsumer, name='add_to_cart'),
]
