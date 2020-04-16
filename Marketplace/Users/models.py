from django.db import models
from django.contrib.auth.models import User


# The Marketplace user. The Django User is used as a building block, but additional information is
# stored in the UserInfo table.
class UserInfo(models.Model):
    phone_number = models.TextField(null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField()


class Address(models.Model):
    country = models.TextField()
    province = models.TextField()
    city = models.TextField()
    street_address = models.TextField()
    postal_code = models.TextField()
    is_default_shipping = models.BooleanField(default=True)
    user = models.ForeignKey(UserInfo, related_name='user_address', on_delete=models.DO_NOTHING)

    def __eq__(self, other):
        if not isinstance(other, Address):
            return False

        return (self.country == other.country and
                self.province == other.province and
                self.city == other.city and
                self.street_address == other.street_address and
                self.postal_code == other.postal_code)
