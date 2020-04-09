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

        cart_db = models.Cart.objects.get(pk=cart_id)
        product_db = models.Product.objects.get(pk=product_id)

        product_already_in_cart = models.CartProduct.objects.filter(product=product_db, cart=cart_db)
        if product_already_in_cart.exists():
            product_already_in_cart = product_already_in_cart.first()
            if product_db.quantity < quantity:
                message = 'Quantity in stock insufficient. You currently have {} in your cart.'.format(product_already_in_cart.quantity)
                message_type = 'Error'
            else:
                product_already_in_cart.quantity += quantity
                product_already_in_cart.save()
                product_db.quantity -= quantity
                product_db.save()
                message = '{} added to your cart. Total in cart: {}'.format(quantity, product_already_in_cart.quantity)
                message_type = 'Success'
        else:
            if product_db.quantity < quantity:
                message = 'Quantity in stock insufficient.'
                message_type = 'Error'
            else:
                models.CartProduct.objects.create(cart=cart_db, product=product_db, quantity=quantity)
                product_db.quantity -= quantity
                product_db.save()
                message = '{} added to your cart.'.format(quantity)
                message_type = 'Success'

        response = {
            'message': message,
            'type': message_type,
            'qtyInStock': product_db.quantity
        }
        self.send(text_data=json.dumps(response))
