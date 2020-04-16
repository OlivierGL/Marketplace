from django.db import models
from Users.models import UserInfo

CATEGORY_CHOICES = (
    ("PAINTING", "Painting"),
    ("SCULPTURE", "Sculpture"),
    ("GARMENT", "Garment"),
    ("JEWELRY", "Jewelry"),
    ("GLASS_ART", "Glass Art"),
)


def get_image_path(instance, filename):
    return 'user-' + str(instance.artist.pk) + '/' + filename


# table with all products. Product rows contain general information. For more specific
# information, see the other complementary models below.
class Product(models.Model):
    artist = models.ForeignKey(UserInfo, related_name='artist', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.IntegerField()
    image = models.FileField(upload_to=get_image_path)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date_posted = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="PAINTING")


# Extra data specific to paintings
class Painting(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    height = models.FloatField()
    width = models.FloatField()
    paint = models.CharField(max_length=50)


# Extra data specific to sculptures
class Sculpture(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    height = models.FloatField()
    material = models.CharField(max_length=500)


# Extra data specific to clothes
class Garment(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=500)
    materials = models.TextField()


# Extra data specific to jewelry
class Jewelry(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    jewels = models.TextField()
    other_materials = models.TextField()


# Extra data specific to glass art
class GlassArt(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    glass_type = models.CharField(max_length=500)
    other_materials = models.TextField()


# Cart table, to which  cart products will be related with cart_id
class Cart(models.Model):
    user = models.OneToOneField(UserInfo, on_delete=models.CASCADE)


# having the Cart intermediary allows to easily get rid of the cart products with
# on_delete=models.CASCADE
class CartProduct(models.Model):
    product = models.ForeignKey(Product, related_name='product_cart', on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, related_name='cart_products', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

