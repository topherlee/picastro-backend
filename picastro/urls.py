from django.urls import path, re_path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    CreateUserAPIView,
    LogoutUserAPIView,
    get_post_list,
    CurrentUserView,
    PostViewSet,        #old API, delete later on
    PostAPIView,
    PostDetailAPIView
)
from django.urls import path, include

from .views import HomePageView

router = DefaultRouter()                #old API, delete later on
router.register("posts", PostViewSet)   #old API, delete later on


urlpatterns = [
    # re_path(r'^auth/login/$',
    #     obtain_auth_token,
    #     name='auth_user_login'),
    re_path(r'^auth/register/$',
        CreateUserAPIView.as_view(),
        name='auth_user_create'),
    re_path(r'^feed/home/$', get_post_list,),   #old API, delete later on
    path('feed/', PostAPIView.as_view(), name='feed_of_posts'),
    path('feed/<int:id>', PostDetailAPIView.as_view(), name='update_delete_posts'),
    path('current_user/',CurrentUserView.as_view(),name='auth_user_current'),
    path('auth/login/refresh/', TokenRefreshView.as_view(), name='auth_login_refresh'),     
    path('auth/login/', TokenObtainPairView.as_view(), name='auth_login'),
    path('auth/logout/', LogoutUserAPIView.as_view(), name='auth_logout'),       #use this to get access and refresh token
    path("", HomePageView.as_view(), name="home"),
    path("", include(router.urls)),     #old API, delete later on
]
