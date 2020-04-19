from django.test import TestCase
from . import models
from Users import models as users_models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your tests here.

class test_market(TestCase):

    def my_setup(self):
        self.user1 = create_user(
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

        self.user2 = create_user(
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

        self.product = models.Product.objects.create(
            artist=self.user_info1,
            name='The Creation of the Sun and the Moon',
            description="It is one of the frescoes from Michelangelo's nine Books of Genesis scenes on the Sistine Chapel ceiling.",
            quantity=3,
            image='Market/thecreation.jpg',
            price=4300.00,
            category="PAINTING"
        )

    # Checks if users can delete other users' products.
    def test_delete_product_wrong_user(self):
        self.my_setup()
        url = reverse('delete_product', kwargs={'pk': self.product.pk})
        self.client.login(username=self.user2.username, password='password123')
        response = self.client.get(url)
        self.assertIs(True, response.status_code == 403)

    # Checks if we get redirected when trying to access a profile page when logged out
    def test_accessing_profiles_loggedout_redirects(self):
        self.my_setup()
        url = reverse('profile', kwargs={'primary_key': self.user1.pk})
        response = self.client.get(url)
        self.assertIs(True, response.status_code == 302)

    # Checks if products get deleted when the seller's user gets deleted
    def test_products_deleted_after_user_deleted(self):
        self.my_setup()
        products = models.Product.objects.filter(artist=self.user_info1)
        self.user1.delete()
        self.assertIs(False, products.exists())
