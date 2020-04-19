from django.db import models
from Users.models import UserInfo
from django.urls import reverse

CATEGORY_CHOICES = (
  ("PAINTING", "Painting"),
  ("SCULPTURE", "Sculpture"),
  ("GARMENT", "Garment"),
  ("JEWELRY", "Jewelry"),
  ("GLASS_ART", "Glass Art"),
)


# Method that returns the path where an image should be stored.
def get_image_path(instance, filename):
  return 'user-' + str(instance.artist.pk) + '/' + filename


# Product object that stores related data.
class Product(models.Model):
  artist = models.ForeignKey(UserInfo, related_name='artist', on_delete=models.CASCADE)
  name = models.CharField(max_length=100)
  description = models.TextField()
  quantity = models.IntegerField()
  image = models.FileField(upload_to=get_image_path)
  price = models.DecimalField(max_digits=6, decimal_places=2)
  date_posted = models.DateTimeField(auto_now_add=True)
  category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="PAINTING")

  def get_absolute_url(self):
    return reverse('profile', kwargs={'primary_key': self.artist.user.pk})



# Cart table, to which  cart products will be related with cart_id
class Cart(models.Model):
  user = models.OneToOneField(UserInfo, on_delete=models.CASCADE)


# having the Cart intermediary allows to easily get rid of the cart products with
# on_delete=models.CASCADE
class CartProduct(models.Model):
  product = models.ForeignKey(Product, related_name='product_cart', on_delete=models.CASCADE)
  cart = models.ForeignKey(Cart, related_name='cart_products', on_delete=models.CASCADE)
  quantity = models.IntegerField(default=1)

