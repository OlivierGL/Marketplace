import json

from channels.generic.websocket import WebsocketConsumer

from . import models


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
    db_product = models.Product.objects.get(pk=product_id)

    # Only happens if the user is not logged in
    if cart_id == '':
      message = 'Please login to your account before adding products to your cart.'
      message_type = 'Error'
      qty_in_cart = 0
    else:
      cart_db = models.Cart.objects.get(pk=cart_id)
      cart_product = models.CartProduct.objects.filter(product=db_product, cart=cart_db)

      # Product is already in cart, must validate and update the quantity
      if cart_product.exists():
        cart_product = cart_product.first()
        message, message_type, qty_in_cart = validate_product_in_cart(db_product, cart_product, quantity)

      # New product to be added in cart
      else:
        # Should never happen because of front-end validations
        if db_product.quantity < quantity:
          message = 'Quantity in stock insufficient.'
          message_type = 'Error'
          qty_in_cart = 0
        else:
          models.CartProduct.objects.create(cart=cart_db, product=db_product, quantity=quantity)
          message = 'Cart updated successfully. Total items in cart: {}'.format(quantity)
          message_type = 'Success'
          qty_in_cart = quantity

    response = {
      'message': message,
      'type': message_type,
      'qtyInStock': db_product.quantity,
      'qtyInCart': qty_in_cart
    }
    self.send(text_data=json.dumps(response))


def validate_product_in_cart(db_product, cart_product, new_quantity):
  # Not enough products in stock (should never happen because of front-end validations...)
  if db_product.quantity < new_quantity:
    message = 'Quantity in stock insufficient. You currently have {} in your cart.'.format(
      cart_product.quantity)
    message_type = 'Error'
    qty_in_cart = cart_product.quantity
  # Quantity in cart has not changed
  elif cart_product.quantity == new_quantity:
    message = 'Quantity in cart has not changed. You currently have {} in your cart.'.format(
      cart_product.quantity)
    message_type = 'Error'
    qty_in_cart = cart_product.quantity
  # Quantity in cart has successfully been updated
  else:
    cart_product.quantity = new_quantity
    cart_product.save()
    message = 'Cart updated successfully. Total items in cart: {}'.format(new_quantity)
    message_type = 'Success'
    qty_in_cart = cart_product.quantity

  return message, message_type, qty_in_cart
