from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.urls import reverse

# def create_user(**params):
#     return get_user_model().objects.create_user(**params)

class ModelTests(TestCase):

    def test_create_user_with(self):
        username = 'operator'
        password = 'operator123'
        user = get_user_model().objects.create_user(
            username = username,
            password = password
        )

        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))

    def test_create_new_superuser(self):
        user = get_user_model().objects.create_superuser(
            username = 'admin',
            password = 'admin123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

# class UserAPITest(TestCase):
#     '''Test the user API'''
#     def setUp(self):
#         self.client = APIClient()

#     def test_create_valid_user(self):
#         '''Testing creating user with valid payload is successful'''
#         payload = {'username': 'testusername', 'password': 'testpassword'}
#         res = self.client.post()