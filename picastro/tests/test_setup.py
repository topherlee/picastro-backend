from rest_framework.test import APITestCase
from django.urls import reverse


class TestSetup(APITestCase):

    def setUp(self):
        self.register_url = reverse('auth_user_create')
        self.login_url = reverse('auth_login')
        self.current_user_url = reverse('auth_user_current')

        self.user_data = {
            "username": "username",
            "password": "password123",
            "first_name": "test_first",
            "last_name": "test_last",
            "email": "test@picastro.com",
            "location": "Dundee_test",
            "userDescription": "long test description",
            "genderIdentifier": "diverse",
        }

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
