from channels.generic.websocket import WebsocketConsumer
from . import models
import json


class ProductConsumer(WebsocketConsumer):
    # Connect. Nothing else to do here since we don't need groups
    def connect(self):
        self.accept()

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        cart_id = text_data_json['cartId']
        product_id = text_data_json['productId']
        quantity = int(text_data_json['quantity'])
        product_db = models.Product.objects.get(pk=product_id)

        qty_in_cart = 0
        if cart_id == '':
            message = 'Please login to your account before adding products to your cart.'
            message_type = 'Error'
        else:
            cart_db = models.Cart.objects.get(pk=cart_id)

            product_already_in_cart = models.CartProduct.objects.filter(product=product_db, cart=cart_db)
            if product_already_in_cart.exists():
                product_already_in_cart = product_already_in_cart.first()
                if product_db.quantity < quantity:
                    message = 'Quantity in stock insufficient. You currently have {} in your cart.'.format(
                        product_already_in_cart.quantity)
                    message_type = 'Error'
                    qty_in_cart = product_already_in_cart.quantity
                elif product_already_in_cart.quantity == quantity:
                    message = 'Quantity in cart has not changed. You currently have {} in your cart.'.format(
                        product_already_in_cart.quantity)
                    message_type = 'Error'
                    qty_in_cart = product_already_in_cart.quantity
                else:
                    product_already_in_cart.quantity = quantity
                    product_already_in_cart.save()
                    message = 'Cart updated successfully. Total items in cart: {}'.format(quantity)
                    message_type = 'Success'
                    qty_in_cart = product_already_in_cart.quantity
            else:
                if product_db.quantity < quantity:
                    message = 'Quantity in stock insufficient.'
                    message_type = 'Error'
                else:
                    models.CartProduct.objects.create(cart=cart_db, product=product_db, quantity=quantity)
                    message = 'Cart updated successfully. Total items in cart: {}'.format(quantity)
                    message_type = 'Success'
                    qty_in_cart = quantity

        response = {
            'message': message,
            'type': message_type,
            'qtyInStock': product_db.quantity,
            'qtyInCart': qty_in_cart
        }
        self.send(text_data=json.dumps(response))
