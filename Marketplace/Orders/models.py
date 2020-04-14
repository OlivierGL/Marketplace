from django.db import models
from Users.models import UserInfo, Address
from Market.models import Product


# Data about an order that has been placed. An order is for a single product.
class Order(models.Model):
    buyer = models.ForeignKey(UserInfo, related_name='buyer', on_delete=models.CASCADE)
    seller = models.ForeignKey(UserInfo, related_name='seller', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    shipping = models.ForeignKey(Address, related_name='shipping_address', on_delete=models.DO_NOTHING)


# an order product that is related to a given order with order_id
class OrderProduct(models.Model):
    product = models.ForeignKey(Product, related_name='order_product', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name='order', on_delete=models.CASCADE)
    quantity = models.IntegerField()
