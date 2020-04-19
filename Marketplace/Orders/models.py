from django.db import models

from Market.models import Product
from Users.models import UserInfo, Address

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
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    fed_taxes_amount = models.DecimalField(max_digits=10, decimal_places=2)
    prov_taxes_amount = models.DecimalField(max_digits=10, decimal_places=2)


# an order product that is related to a given order with order_id
class OrderProduct(models.Model):
    product = models.ForeignKey(Product, related_name='product_order', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name='order_products', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price_paid = models.DecimalField(max_digits=10, decimal_places=2)
