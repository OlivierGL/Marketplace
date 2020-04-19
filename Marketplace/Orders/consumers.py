import json

from channels.generic.websocket import WebsocketConsumer

from Market import models as market_models
from Users import models as user_models
from . import models


class OrdersConsumer(WebsocketConsumer):
    # Connect. Nothing else to do here since we don't need groups
    def connect(self):
        self.accept()

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        buyer = user_models.UserInfo.objects.get(user_id=text_data_json['buyerId'])
        cart_products = market_models.CartProduct.objects.filter(cart=buyer.cart, quantity__gt=0)

        errors = validate_products_in_stock(cart_products)
        if errors:
            # Some product in cart has gone out of stock
            self.send(text_data=json.dumps({'errors': errors}))
        else:
            create_order_and_order_products(text_data_json, buyer, cart_products)
            # Send empty errors list
            self.send(text_data=json.dumps([]))


def validate_products_in_stock(cart_products):
    errors = []
    for cart_product in cart_products:
        db_product = cart_product.product
        if cart_product.quantity > db_product.quantity:
            errors.append(db_product.name)
    return errors


def create_order_and_order_products(text_data_json, buyer, cart_products):
    # Create order
    paypal_invoice = text_data_json['paypalInvoice']
    total_amount = text_data_json['totalAmount']
    subtotal_amount = text_data_json['subtotalAmount']
    prov_taxes = text_data_json['provTaxes']
    fed_taxes = text_data_json['fedTaxes']
    shipping_address = buyer.user_address.get(is_default_shipping=True)
    order = models.Order.objects.create(
        buyer=buyer,
        shipping=shipping_address,
        payPalInvoice=paypal_invoice,
        total_amount=total_amount,
        subtotal_amount=subtotal_amount,
        fed_taxes_amount=fed_taxes,
        prov_taxes_amount=prov_taxes
    )
    # Create order_products
    for cart_product in cart_products:
        db_product = cart_product.product
        db_product.quantity -= cart_product.quantity
        db_product.save()
        models.OrderProduct.objects.create(
            product=db_product,
            order=order,
            quantity=cart_product.quantity,
            price_paid=db_product.price
        )
