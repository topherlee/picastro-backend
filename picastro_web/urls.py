from django.urls import path, re_path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    
    HomePageView,
    DashboardView,
    CreatePostView
)
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import HomePageView
from . import views




urlpatterns = [
    #use this to get access and refresh token
    path("", HomePageView.as_view(), name="home"),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    #path('post/', views.post_image, name='postimage'),
    path("post/", CreatePostView.as_view(), name="add_post"),
     #path('edit/', views.post_image, name='edit'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
