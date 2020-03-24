from django.db import models
from django.contrib.auth.models import User 


# table with all products. Product rows contain general information. For more specific
# information, see the other complementary models below.  
class Product(models.Model):
  name = models.CharField(max_length=100)
  description = models.TextField()
  quantity = models.IntegerField()
  image = models.TextField()
  price = models.FloatField()
  date_posted = models.DateTimeField(auto_now_add=True)
  category = models.CharField(max_length=50)

# Extra data specific to paintings
class Painting(models.Model):
  product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
  height = models.FloatField()
  width = models.FloatField()
  paint = models.CharField(max_length=50)

# Extra data specific to sculptures
class Sculpture(models.Model):
  product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
  height = models.FloatField()
  material = models.CharField(max_length=500)

# Extra data specific to clothes
class Garment(models.Model):
  product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
  size = models.CharField(max_length=500)
  materials = models.TextField()

# Extra data specific to jewelry
class Jewelry(models.Model):
  product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
  jewels = models.TextField()
  other_materials = models.TextField()

# Extra data specific to glass art
class GlassArt(models.Model):
  product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
  glass_type = models.CharField(max_length=500)
  other_materials = models.TextField()

# Cart table, to which  cart products will be related with cart_id
class Cart(models.Model):
  user_id = models.ForeignKey(User, on_delete=models.CASCADE)

# having the Cart intermediary allows to easily get rid of the cart products with 
# on_delete=models.CASCADE
class CartProduct(models.Model):
  product_id = models.ForeignKey(Product, related_name='cart_product', on_delete=models.CASCADE)
  cart_id = models.ForeignKey(Cart, related_name='cart', on_delete=models.CASCADE)
  quantity = models.IntegerField()

# Data about an order that has been placed. An order is for a single product. 
class Order(models.Model):
  buyer_id = models.ForeignKey(User, related_name='buyer', on_delete=models.CASCADE)
  seller_id = models.ForeignKey(User, related_name='seller', on_delete=models.CASCADE)
  timestamp = models.DateTimeField(auto_now_add=True)
  shipping = models.TextField()

# an order product that is related to a given order with order_id
class OrderProduct(models.Model):
  product_id = models.ForeignKey(Product, related_name='order_product', on_delete=models.CASCADE)
  order_id = models.ForeignKey(Order, related_name='order', on_delete=models.CASCADE)
  quantity = models.IntegerField()


# Chat table that only stores the two users in a chat 
class Chat(models.Model):
  user1_id = models.ForeignKey(User, related_name='user1', on_delete=models.CASCADE)
  user2_id = models.ForeignKey(User, related_name='user2', on_delete=models.CASCADE)
  
# table with all messages (can be associated with a chat by using the chat_id column)
class Message(models.Model):
  chat_id = models.IntegerField()
  user_id = models.IntegerField()
  message = models.TextField()
  timestamp = models.DateTimeField(auto_now_add=True)





