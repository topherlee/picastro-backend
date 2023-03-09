from django.urls import path, re_path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CreateUserAPIView, LogoutUserAPIView, get_post_list, CurrentUserView
from django.urls import path

from .views import HomePageView

urlpatterns = [
    # re_path(r'^auth/login/$',
    #     obtain_auth_token,
    #     name='auth_user_login'),
    re_path(r'^auth/register/$',
        CreateUserAPIView.as_view(),
        name='auth_user_create'),
    re_path(r'^auth/logout/$',
        LogoutUserAPIView.as_view(),
        name='auth_user_logout'),
    re_path(r'^feed/home/$', get_post_list,),
    path('current_user/',CurrentUserView.as_view(),name='auth_user_current'),
    path('token/access/', TokenRefreshView.as_view(), name='token_get_access'),     
    path('token/both/', TokenObtainPairView.as_view(), name='token_obtain_pair'),       #use this to get access and refresh token
    path("", HomePageView.as_view(), name="home"),
]
