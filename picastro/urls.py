from django.urls import path, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf.urls.static import static
from django.conf import settings

from .views import (
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
from django.urls import path, include


urlpatterns = [
    re_path(r'^auth/register/$',
            CreateUserAPIView.as_view(),
            name='auth_user_create'),
    path('auth/login/refresh/', TokenRefreshView.as_view(), name='auth_login_refresh'),     
    path('auth/login/', TokenObtainPairView.as_view(), name='auth_login'),
    path('auth/email-verify/', VerifyEmail.as_view(), name='email-verify'),
    path('auth/pw-reset/', RequestPasswordResetEmail.as_view(), name='request_password-reset'),
    path('auth/reset/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('auth/logout/', LogoutUserAPIView.as_view(), name='auth_logout'),   # use this to get access and refresh token
    path('current_user/', CurrentUserView.as_view(), name='auth_user_current'),
    path('user/<int:id>', UserProfileAPIView.as_view(), name='user_profile'),
    path('feed/', PostAPIView.as_view(), name='feed_of_posts'),
    path('feed/<int:id>', PostDetailAPIView.as_view(), name='update_delete_posts'),
    # path('like/<int:user_id>/<int:image_id>', ImageLikeAPIView.as_view(), name='image_like'),
    path('like/<int:post>', ImageLikeAPIView.as_view(), name='image_like'),
    # path('dislike/<int:user>/<int:post>', ImageDislikeAPIView.as_view(), name='image_dislike'),
    path('dislike/<int:post>', ImageDislikeAPIView.as_view(), name='image_dislike'),
    path('comments/',CommentCreateAPIView.as_view(),name='comment_create'),
    path('comments/<int:post_id>',CommentListAPIView.as_view(),name='comment_list'),
    path('comment/<int:id>',CommentUpdateDestroyAPIView.as_view(),name='comment_ud'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
