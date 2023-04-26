from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.test import SimpleTestCase
from django.urls import reverse, resolve

from picastro.views import (
    CreateUserAPIView,
    LogoutUserAPIView,
    CurrentUserView,
    PostAPIView,
    PostDetailAPIView,
    UserProfileAPIView,
    PasswordTokenCheckAPI,
    RequestPasswordResetEmail,
    VerifyEmail
)

class ApiUrlsTests(SimpleTestCase):

    def test_auth_user_create_is_resolved(self):
        url = reverse('auth_user_create')
        self.assertEqual(resolve(url).func.view_class, CreateUserAPIView)

    def test_feed_is_resolved(self):
        url = reverse('feed_of_posts')
        self.assertEqual(resolve(url).func.view_class, PostAPIView)

    # def test_that_update_delete_posts_is_resolved(self):
    #     url = reverse('update_delete_posts')
    #     self.assertEqual(resolve(url).func.view_class, PostDetailAPIView)

    def test_current_user_is_resolved(self):
        url = reverse('auth_user_current')
        self.assertEqual(resolve(url).func.view_class, CurrentUserView)

    # def test_user_profile_is_resolved(self):
    #     url = reverse('user_profile')
    #     self.assertEqual(resolve(url).func.view_class, UserProfileAPIView)

    def test_auth_login_refresh_is_resolved(self):
        url = reverse('auth_login_refresh')
        self.assertEqual(resolve(url).func.view_class, TokenRefreshView)

    def test_auth_login_is_resolved(self):
        url = reverse('auth_login')
        self.assertEqual(resolve(url).func.view_class, TokenObtainPairView)

    def test_email_verify_is_resolved(self):
        url = reverse('email-verify')
        self.assertEqual(resolve(url).func.view_class, VerifyEmail)

    def test_request_password_reset_is_resolved(self):
        url = reverse('request_password-reset')
        self.assertEqual(resolve(url).func.view_class, RequestPasswordResetEmail)

    # def test_password_reset_confirm_is_resolved(self):
    #     url = reverse('password-reset-confirm')
    #     self.assertEqual(resolve(url).func.view_class, PasswordTokenCheckAPI)

    def test_auth_logout_is_resolved(self):
        url = reverse('auth_logout')
        self.assertEqual(resolve(url).func.view_class, LogoutUserAPIView)
