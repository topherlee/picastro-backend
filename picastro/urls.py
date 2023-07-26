from django.urls import path, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf.urls.static import static
from django.conf import settings

from .views import (
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
    CommentCreateAPIView,
    CommentListAPIView,
    CommentUpdateDestroyAPIView
)
from django.urls import path, include


urlpatterns = [
    re_path(r'^auth/register/$',
            CreateUserAPIView.as_view(),
            name='auth_user_create'),
    path('feed/', PostAPIView.as_view(), name='feed_of_posts'),
    path('feed/<int:id>', PostDetailAPIView.as_view(), name='update_delete_posts'),
    path('current_user/', CurrentUserView.as_view(), name='auth_user_current'),
    path('user/<int:id>', UserProfileAPIView.as_view(), name='user_profile'),
    path('auth/login/refresh/', TokenRefreshView.as_view(), name='auth_login_refresh'),     
    path('auth/login/', TokenObtainPairView.as_view(), name='auth_login'),
    path('auth/email-verify/', VerifyEmail.as_view(), name='email-verify'),
    path('auth/pw-reset/', RequestPasswordResetEmail.as_view(), name='request_password-reset'),
    path('auth/reset/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('auth/logout/', LogoutUserAPIView.as_view(), name='auth_logout'),   # use this to get access and refresh token
    path("", HomePageView.as_view(), name="home"),
    path('comments/',CommentCreateAPIView.as_view(),name='comment_create'),
    path('comments/<int:post_id>',CommentListAPIView.as_view(),name='comment_list'),
    path('comment/<int:comment_id>',CommentUpdateDestroyAPIView.as_view(),name='comment_ud'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
