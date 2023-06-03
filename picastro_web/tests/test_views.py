import json
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from picastro.models import Post, StarCamp
from picastro_web.forms import LoginForm, PostForm, UserRegistrationForm
from picastro_web.tests.test_setup import TestSetup


class TestWebRegisterView(TestSetup):

    def test_register_POST(self):
        response = self.client.post(self.register_url)
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_register_GET(self):
        response = self.client.get(self.register_url)
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')


class TestWebLoginView(TestSetup):

    def test_user_login_POST(self):
        response = self.client.post(self.login_url)
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_user_login_GET(self):
        response = self.client.get(self.login_url)
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')


class TestWebPostView(TestSetup):

    def test_CreatePostView_POST_without_login(self):
        response = self.client.post(self.posts_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url + '?next=%2Fpicastro%2Fpost%2F')

    def test_CreatePostView_POST_with_login(self):
        self.client.post(self.login_url, self.login_data)
        response = self.client.get(self.posts_url, self.post_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'picastro_web/post.html')

    def test_CreatePostView_GET_without_login(self):
        response = self.client.get(self.posts_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url + '?next=%2Fpicastro%2Fpost%2F')

    def test_CreatePostView_GET_with_login(self):
        res1 = self.client.post(self.login_url, self.login_data)
        response = self.client.get(self.posts_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'picastro_web/post.html')


class TestWebDashboardView(TestSetup):

    def test_DashboardView_without_login(self):
        response = self.client.get(self.dashboard_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url + '?next=%2Fpicastro%2Fdashboard%2F')
        
    def test_DashboardView_with_login(self):
        res1 = self.client.post(self.login_url, self.login_data)
        # print("res1", res1)
        response = self.client.get(self.dashboard_url)
        # print("response", response)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'picastro_web/dashboard.html')
    

class TestWebHomepageView(TestSetup):

    def test_HomePageView(self):
        response = self.client.get(self.home_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'picastro_web/home.html')
