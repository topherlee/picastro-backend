from rest_framework.test import APITestCase
from django.urls import reverse

from picastro.models import StarCamp


class TestSetup(APITestCase):

    def setUp(self):
        
        self.register_url = reverse('auth_user_create')
        self.login_url = reverse('auth_login')
        self.current_user_url = reverse('auth_user_current')
        self.posts_url = reverse('feed_of_posts')

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

        self.post_data = {
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

        self.starcamp_data = {
            "starCampName": "Aberdeen",
            "starCampLocation": "Aberdeen"
        }

        self.star_camp1 = StarCamp.objects.create(
            starCampName = "Glasgow",
            starCampLocation = "Glasgow"
        )

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
