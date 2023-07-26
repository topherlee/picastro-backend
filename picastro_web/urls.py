from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    HomePageView,
    DashboardView,
    CreatePostView
)
from . import views


urlpatterns = [
    #use this to get access and refresh token
    path("", HomePageView.as_view(), name="home"),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path("post/", CreatePostView.as_view(), name="add_post"),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
