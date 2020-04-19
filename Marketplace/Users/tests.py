from django.contrib.auth.models import User
from django.test import TestCase

from .models import UserInfo, Rating


def create_user(username):
    user = User.objects.create_user(
        username=username,
        email='stub@gmail.com',
        password='password321',
        first_name='first',
        last_name='last'
    )

    user_info = UserInfo.objects.create(
        user=user,
        phone_number=5557779999
    )

    return user, user_info


def create_rating(rating, receiver, giver):
    rating_db = Rating.objects.create(
        receiver=receiver,
        giver=giver,
        rating=rating
    )

    return rating_db


# Create your tests here.
class TestUsers(TestCase):

    def setup(self):
        self.receiver, self.receiver_info = create_user("receiver")
        self.giver1, self.giver1_info = create_user("giver1")
        self.giver2, self.giver2_info = create_user("giver2")
        self.giver3, self.giver3_info = create_user("giver3")

        create_rating(1, self.receiver_info, self.giver1_info)
        create_rating(2, self.receiver_info, self.giver2_info)
        create_rating(5, self.receiver_info, self.giver3_info)

    def test_user_with_ratings_rating_returns_average_of_all_ratings(self):
        self.setup()
        rating = self.receiver_info.rating
        self.assertEqual(2.67, rating)

    def test_user_without_ratings_rating_returns_zero(self):
        self.setup()
        rating = self.giver1_info.rating
        self.assertEqual(0, rating)
