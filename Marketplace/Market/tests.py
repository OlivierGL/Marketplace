from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from Users import models as users_models
from . import models


class TestMarket(TestCase):

    # Method that sets up required database entries for the tests
    def my_setup(self):
        # Creating user1
        self.user1 = User.objects.create_user(
            username='stub1',
            email='stub@gmail.com',
            password='password321',
            first_name='first',
            last_name='last'
        )

        self.user_info1 = users_models.UserInfo.objects.create(
            user=self.user1,
            phone_number=5557779999
        )

        # Creating user2
        self.user2 = User.objects.create_user(
            username='stub2',
            email='stub@gmail.com',
            password='password123',
            first_name='first',
            last_name='last'
        )

        self.user_info2 = users_models.UserInfo.objects.create(
            user=self.user2,
            phone_number=5557779999
        )

        # Creating a product which is sold by user1
        self.product = models.Product.objects.create(
            artist=self.user_info1,
            name='The Creation of the Sun and the Moon',
            description="It is one of the frescoes from Michelangelo's nine Books of Genesis scenes on the Sistine Chapel ceiling.",
            quantity=3,
            image='Market/thecreation.jpg',
            price=4300.00,
            category="PAINTING"
        )

    # Checks that users can't delete other users' products.
    def test_delete_product_wrong_user(self):
        self.my_setup()
        # Url that causes the deletion of the product with primary key pk
        url = reverse('delete_product', kwargs={'pk': self.product.pk})
        # Loging in as a user that isn't selling the product
        self.client.login(username=self.user2.username, password='password123')
        # Accessing the url
        response = self.client.get(url)
        # Verifying that the url returns Forbidden: 403
        self.assertIs(True, response.status_code == 403)

    # Checks that users get redirected when trying to access a profile page when logged out
    def test_accessing_profiles_loggedout_redirects(self):
        self.my_setup()
        # Url address for some random user
        url = reverse('profile', kwargs={'primary_key': self.user1.pk})
        # Accessing the url
        response = self.client.get(url)
        # Checking that the response code is 302 (Redirected)
        self.assertIs(True, response.status_code == 302)

    # Checks that products get deleted when the seller's user gets deleted
    def test_products_deleted_after_user_deleted(self):
        self.my_setup()
        # Getting the products of user1 (one created by my_setup())
        products = models.Product.objects.filter(artist=self.user_info1)
        self.user1.delete()
        # Verifying that none of the products exist anymore
        self.assertIs(False, products.exists())
