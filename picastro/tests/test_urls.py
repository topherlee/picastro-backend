from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.test import SimpleTestCase
from django.urls import reverse, resolve

from picastro.views import (
    HomePageView,
    CreateUserAPIView,
    LogoutUserAPIView,
    CurrentUserView,
    PostAPIView,
    PostDetailAPIView,
    UserProfileAPIView,
    PasswordTokenCheckAPI,
    RequestPasswordResetEmail,
    VerifyEmail,
    ImageLikeAPIView,
    ImageDislikeAPIView,
    CommentCreateAPIView,
    CommentListAPIView,
    CommentUpdateDestroyAPIView
)

class ApiUrlsTests(SimpleTestCase):

    def test_home_is_resolved(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func.view_class, HomePageView)

    def test_auth_user_create_is_resolved(self):
        url = reverse('auth_user_create')
        self.assertEqual(resolve(url).func.view_class, CreateUserAPIView)

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

    def test_password_reset_confirm_is_resolved(self):
        url = reverse('password-reset-confirm', args=[1, 1])
        self.assertEqual(resolve(url).func.view_class, PasswordTokenCheckAPI)

    def test_auth_logout_is_resolved(self):
        url = reverse('auth_logout')
        self.assertEqual(resolve(url).func.view_class, LogoutUserAPIView)
    
    def test_current_user_is_resolved(self):
        url = reverse('auth_user_current')
        self.assertEqual(resolve(url).func.view_class, CurrentUserView)

    def test_user_profile_is_resolved(self):
        url = reverse('user_profile', args=[1])
        self.assertEqual(resolve(url).func.view_class, UserProfileAPIView)

    def test_feed_is_resolved(self):
        url = reverse('feed_of_posts')
        self.assertEqual(resolve(url).func.view_class, PostAPIView)

    def test_that_update_delete_posts_is_resolved(self):
        url = reverse('update_delete_posts', args=[1])
        self.assertEqual(resolve(url).func.view_class, PostDetailAPIView)

    def test_image_like_is_resolved(self):
        url = reverse('image_like', args=[1])
        self.assertEqual(resolve(url).func.view_class, ImageLikeAPIView)

    def test_image_dislike_is_resolved(self):
        url = reverse('image_dislike', args=[1])
        self.assertEqual(resolve(url).func.view_class, ImageDislikeAPIView)

    def test_comment_create_is_resolved(self):
        url = reverse('comment_create')
        self.assertEqual(resolve(url).func.view_class, CommentCreateAPIView)

    def test_comment_list_is_resolved(self):
        url = reverse('comment_list', args=[1])
        self.assertEqual(resolve(url).func.view_class, CommentListAPIView)

    def test_comment_ud_is_resolved(self):
        url = reverse('comment_ud', args=[1])
        self.assertEqual(resolve(url).func.view_class, CommentUpdateDestroyAPIView)
