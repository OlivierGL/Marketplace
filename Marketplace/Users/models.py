from django.db import models
from django.contrib.auth.models import User


class Address(models.Model):
    country = models.TextField()
    province = models.TextField()
    city = models.TextField()
    street_address = models.TextField()
    postal_code = models.TextField()


# The Marketplace user. The Django User is used as a building block, but additional information is
# stored in the UserInfo table.
class UserInfo(models.Model):
    phone_number = models.TextField(null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
