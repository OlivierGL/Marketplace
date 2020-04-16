from django.db import models
from Users.models import UserInfo, Address
from Market.models import Product

ORDER_STATUS = (
    ("PAID", "Paid"),
    ("CANCELED", "Canceled"),
    ("PENDING", "Pending")
)


# Data about an order that has been placed. An order is for a single product.
class Order(models.Model):
    buyer = models.ForeignKey(UserInfo, related_name='buyer_orders', on_delete=models.CASCADE)
    payPalInvoice = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    shipping = models.ForeignKey(Address, related_name='shipping_address', on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=10, choices=ORDER_STATUS, default="PENDING")


# an order product that is related to a given order with order_id
class OrderProduct(models.Model):
    product = models.ForeignKey(Product, related_name='product_order', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name='order_products', on_delete=models.CASCADE)
    quantity = models.IntegerField()
