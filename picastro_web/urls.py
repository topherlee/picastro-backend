from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from .views import (
    HomePageView,
    DashboardView,
    CreatePostView
)
from . import views


urlpatterns = [
    path("", HomePageView.as_view(), name="web_home"),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("post/", CreatePostView.as_view(), name="add_post"),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
