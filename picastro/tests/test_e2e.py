from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from picastro.tests.test_setup import TestSetup
from picastro.models import PicastroUser, StarCamp


class TestRegistration(TestSetup):

    def test_user_registration(self):
        # star_camp = self.create_test_starcamp()
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(PicastroUser.objects.count(), 1)
        

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
    def test_should_create_post(self):
        self.authenticate()
        
        response = self.client.post(self.posts_url, self.post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        res2 = self.client.get(self.posts_url)


class TestRUDPost(TestSetup):

    def authenticate(self):
        self.client.post(self.register_url, self.user_data)

        response = self.client.post(self.login_url, self.user_data)
        print(f"Token authenticate() {response.data['access']}")

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {response.data['access']}")
    
    def test_retrieve_posts(self):
        self.authenticate()

        self.client.post(self.posts_url, self.post_data)

        response = self.client.get(self.post_details_url, args=[1])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['astroName'], self.post_data['astroName'])


class TestImageLike(TestSetup):

    def authenticate(self):
        self.client.post(self.register_url, self.user_data)

        response = self.client.post(self.login_url, self.user_data)
        print(f"Token authenticate() {response.data['access']}")

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {response.data['access']}")
    
    def test_image_like(self):
        user = self.create_test_user()
        post = self.create_test_post(user)
        self.client.login(self.login_data['username'], self.login_data['password'])

        response = self.client.post(reverse('image_like', args=[user.id, post.id]))
        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.user_data['username'])
        self.assertEqual(response.data['post'], "1")
        
    def test_like_image(self):
        self.authenticate()

        self.client.post(self.posts_url, self.post_data)

        response = self.client.post(self.image_like_url, args=[1, 1])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.user_data['username'])
        self.assertEqual(response.data['post'], "1")
        