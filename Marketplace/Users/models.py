from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


# The Marketplace user. The Django User is used as a building block, but additional information is
# stored in the UserInfo table.
class UserInfo(models.Model):
    phone_number = models.TextField(null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def _get_rating(self):
        count = self.ratings_received.count()
        ratings_sum = 0
        for rating_received in self.ratings_received:
            ratings_sum += rating_received.rating

        return ratings_sum / count

    rating = property(_get_rating)


class Rating(models.Model):
    receiver = models.ForeignKey(UserInfo, related_name="ratings_received", on_delete=models.CASCADE)
    giver = models.ForeignKey(UserInfo, related_name="ratings_given", on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])


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
