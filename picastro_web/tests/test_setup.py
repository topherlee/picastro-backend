from rest_framework.test import APITestCase
from django.urls import reverse
from django.test import TestCase, Client
from tempfile import NamedTemporaryFile

from picastro.models import StarCamp, PicastroUser


class TestSetup(TestCase):

    def setUp(self):
        self.client = Client()

        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.posts_url = reverse('add_post')
        self.dashboard_url = reverse('dashboard')
        self.home_url = reverse('web_home')

        self.user_data = {
            "username": "username",
            "password": "password123",
            "first_name": "test_first",
            "last_name": "test_last",
            "email": "test@picastro.com"
        }

        self.login_data = {
            "username": "username",
            "password": "password123"
        }
        
        self.user_profile_data = {
            "location": "Dundee_test",
            "userDescription": "long test description",
            "genderIdentifier": "diverse",
        }

        self.starcamp_data = {
            "starCampName": "Aberdeen",
            "starCampLocation": "Aberdeen"
        }

        self.post_data = {
            "image": NamedTemporaryFile(suffix='.jpg', prefix="test_img_"),
            "astroNameShort": "IC442",
            "astroName": "Star #1",
            "exposureTime": "6 hrs",
            "moonPhase": "50%",
            "cloudCoverage": "10%",
            "bortle": "3",
            "imageDescription": "The Omega Nebula",
            "imageCategory": "nebula",
            "poster": "1",
        }

        return super().setUp()

    def create_test_user(self):
        user = PicastroUser.objects.create_user(
            username = "username",
            password = "password123",
            first_name = "test_first",
            last_name = "test_last",
            email = "test@picastro.com", 
        )
        return user

    def create_test_starcamp(self):
        starcamp = StarCamp.objects.create(
            starCampName = "Aberdeen",
            starCampLocation = "Aberdeen"
        )
        return starcamp

    def tearDown(self):
        return super().tearDown()
