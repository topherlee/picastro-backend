from django.test import SimpleTestCase
from django.urls import reverse, resolve
from django.contrib.auth import views as auth_views

from picastro_web.views import (
    HomePageView,
    DashboardView,
    CreatePostView,
    user_login,
    register
)
from picastro_web import views


class UrlsTests(SimpleTestCase):

    def test_home_is_resolved(self):
        url = reverse('web_home')
        self.assertEqual(resolve(url).func.view_class, HomePageView)

    def test_login_is_resolved(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, auth_views.LoginView)

    def test_logout_is_resolved(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func.view_class, auth_views.LogoutView)

    def test_register_is_resolved(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func, views.register)

    def test_add_post_is_resolved(self):
        url = reverse('add_post')
        self.assertEqual(resolve(url).func.view_class, CreatePostView)

    def test_dashboard_is_resolved(self):
        url = reverse('dashboard')
        self.assertEqual(resolve(url).func.view_class, DashboardView)
