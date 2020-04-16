from channels.generic.websocket import WebsocketConsumer
from Users import models as user_models
from Market import models as market_models
from . import models
import json


def validate_products_in_stock(cart_products):
    errors = []
    for cart_product in cart_products:
        db_product = cart_product.product
        if cart_product.quantity > db_product.quantity:
            cart_product.quantity = db_product.quantity
            cart_product.save()
            errors.append(db_product.name)
    return errors


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
            # Create order
            paypal_invoice = text_data_json['paypalInvoice']
            shipping_address = buyer.user_address.get(is_default_shipping=True)
            order = models.Order.objects.create(
                buyer=buyer,
                shipping=shipping_address,
                payPalInvoice=paypal_invoice
            )
            # Create order_products
            for cart_product in cart_products:
                db_product = cart_product.product
                db_product.quantity -= cart_product.quantity
                db_product.save()
                models.OrderProduct.objects.create(
                    product=db_product,
                    order=order,
                    quantity=cart_product.quantity
                )

            # Send empty errors list
            self.send(text_data=json.dumps([]))
