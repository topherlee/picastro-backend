from django.urls import path, re_path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import(
    CreateUserAPIView,
    LogoutUserAPIView,
    get_post_list,
    CurrentUserView,
    CommentViewSet,
    PostAPIView,
    PostDetailAPIView,
    UserProfileAPIView,
    CommentCreateAPIView,
    CommentListAPIView,
    CommentUpdateDestroyAPIView
)
from django.urls import path, include

from .views import HomePageView


urlpatterns = [
    re_path(r'^auth/register/$',
        CreateUserAPIView.as_view(),
        name='auth_user_create'),
    path('feed/', PostAPIView.as_view(), name='feed_of_posts'),
    path('feed/<int:id>', PostDetailAPIView.as_view(), name='update_delete_posts'),
    path('current_user/',CurrentUserView.as_view(),name='auth_user_current'),
    path('user/<int:id>',UserProfileAPIView.as_view(),name='user_profile'),
    path('auth/login/refresh/', TokenRefreshView.as_view(), name='auth_login_refresh'),     
    path('auth/login/', TokenObtainPairView.as_view(), name='auth_login'),
    path('auth/logout/', LogoutUserAPIView.as_view(), name='auth_logout'),       #use this to get access and refresh token
    path("", HomePageView.as_view(), name="home"),
    path('comments/',CommentCreateAPIView.as_view(),name='comment_create'),
    path('comments/<int:post_id>',CommentListAPIView.as_view(),name='comment_list'),
    path('comment/<int:comment_id>',CommentUpdateDestroyAPIView.as_view(),name='comment_ud'),

]
