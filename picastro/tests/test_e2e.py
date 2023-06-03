from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

from picastro.tests.test_setup import TestSetup
from picastro.models import UserProfile, StarCamp


class TestRegistration(TestSetup):

    def test_user_registration(self):
        # StarCamp.objects.create(self.starcamp_data)
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(UserProfile.objects.count(), 1)


class TestListCreatePosts(TestSetup):

    def authenticate(self):
        self.client.post(self.register_url, self.user_data)

        response = self.client.post(self.login_url, self.user_data)
        print(f"Token authenticate() {response.data['access']}")

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {response.data['access']}")
        # print(f"Test sentence {response.data['access']}")
    
    def test_not_create_post_without_authentication(self):
        response = self.client.post(self.posts_url, self.post_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # test not yet working
    # def test_should_create_post(self):
    #     self.authenticate()
    #     
    #     response = self.client.post(self.posts_url, self.post_data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
