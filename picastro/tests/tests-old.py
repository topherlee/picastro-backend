from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

# Create your tests here.

class TestListCreatePosts(APITestCase):

    def authenticate(self):
        self.client.post(reverse('auth_user_create'), {
            "username": "username",
            "password": "password123",
            "first_name": "test_first",
            "last_name": "test_last",
            "email": "test@picastro.com",
            "location": "Dundee_test",
            "userDescription": "long test description",
            "genderIdentifier": "diverse",
        })

        response = self.client.post(reverse('auth_login'), {
            "username": "username",
            "password": "password123",
        })
        print(f"Token {response.data['access']}")

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {response.data['access']}")
        print(f"TEst sentence {response.data['access']}")
    

    def test_not_create_post_without_authentication(self):
        sample_post = {
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
        response = self.client.post(reverse('feed_of_posts'), sample_post)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_should_create_post(self):
        self.authenticate()
        sample_post = {
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
        response = self.client.post(reverse('feed_of_posts'), sample_post)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

