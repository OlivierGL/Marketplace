from django.db import models
from django.contrib.auth.models import User


# The Marketplace user. The Django User is used as a building block, but additional information is
# stored in the UserInfo table.
class UserInfo(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  rating = models.IntegerField()
  address = models.TextField()
