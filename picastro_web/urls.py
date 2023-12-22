from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from .views import (
    HomePageView,
    DashboardView,
    CreatePostView,
    VerifyEmail,
    Payment,
    # PaymentCheckView,
    PaymentPending,
    PaymentSuccessful,
    PaymentFailed,
    # StripeWebhook
)
from . import views


urlpatterns = [
    path("", HomePageView.as_view(), name="web_home"),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path("post/", CreatePostView.as_view(), name="add_post"),
    path('auth/email-verify/', VerifyEmail.as_view(), name='email-verify'),
    # path('pay_check/', PaymentCheckView.as_view(), name='pay_check'),
    path('pay_subscription/', Payment.as_view(), name='pay_subscription'),
    path('payment_pending/', PaymentPending.as_view(), name='payment_pending'),
    path('payment_successful/', PaymentSuccessful.as_view(), name='payment_successful'),
    path('payment_failed/', PaymentFailed.as_view(), name='payment_failed'),
    path('config/', views.stripe_config),
    path('create-checkout-session/', views.create_checkout_session),
    path('webhook/', views.stripe_webhook),
    # path('payment_success_webhook/', StripeWebhook.as_view(), name='payment_success_webhook')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
