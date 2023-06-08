from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from tempfile import NamedTemporaryFile
from io import BytesIO

from picastro.models import StarCamp, Post, UserProfile

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

        self.starcamp_data1 = {
            "starCampName": "Aberdeen",
            "starCampLocation": "Aberdeen"
        }

        self.starcamp_data2 = {
            "starCampName": "Glasgow",
            "starCampLocation": "Glasgow"
        }

        return super().setUp()

    def create_test_user(self):
        user = User.objects.create_user(
            username = "username",
            password = "password123",
            first_name = "test_first",
            last_name = "test_last",
            email = "test@picastro.com", 
        )
        return user

    def create_test_user_profile(self, user):
        user_profile = UserProfile.objects.create(
            location = "Dundee_test",
            userDescription = "long test description",
            genderIdentifier = "diverse",
            user=user.id
        )
        return user_profile

    def create_test_starcamp(self):
        starcamp = StarCamp.objects.create(
            starCampName = "Aberdeen",
            starCampLocation = "Aberdeen"
        )
        return starcamp
    
    def create_test_post(self, user):
        post = Post.objects.create(
            image = NamedTemporaryFile(suffix='.jpg', prefix="test_img_"),
            astroNameShort = "IC442",
            astroName = "Star #1",
            exposureTime = "6 hrs",
            moonPhase = "50%",
            cloudCoverage = "10%",
            bortle = "3",
            imageDescription = "The Omega Nebula",
            imageCategory = "nebula",
            poster = user,
        )
        return post

    def tearDown(self):
        return super().tearDown()
