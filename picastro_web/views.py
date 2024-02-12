import jwt
import stripe
import time
from datetime import datetime, timezone, timedelta
from django.conf import settings
from django.shortcuts import render
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic import ListView, CreateView
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http.response import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from picastro.models import Post, PicastroUser
from .forms import LoginForm, PostForm, UserRegistrationForm


class HomePageView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Post
    ordering_fields = ['id', 'imageCategory', 'pub_date', 'poster']
    ordering = '-pub_date'
    template_name = "picastro_web/home.html"

    def test_func(self):
        return self.request.user.subscriptionExpiry > datetime.now(timezone.utc)

    def handle_no_permission(self):
        return redirect(reverse('pay_subscription'))


class DashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Post
    ordering_fields = ['id', 'imageCategory', 'pub_date', 'poster']
    ordering = '-pub_date'
    template_name = "picastro_web/dashboard.html"

    def get_queryset(self):
        print(self.request.user)
        return Post.objects.filter(poster__username__contains=self.request.user)

    def test_func(self):
        return self.request.user.subscriptionExpiry > datetime.now(timezone.utc)

    def handle_no_permission(self):
        return redirect(reverse('pay_subscription'))


class CreatePostView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "picastro_web/post.html"
    success_url = reverse_lazy("dashboard")

    def test_func(self):
        return self.request.user.subscriptionExpiry > datetime.now(timezone.utc)

    def handle_no_permission(self):
        return redirect(reverse('pay_subscription'))


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request,
                          'registration/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'registration/register.html',
                  {'user_form': user_form})


class VerifyEmail(TemplateView):
    template_name = "picastro_web/verify_email"
    
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user = PicastroUser.objects.get(id=payload['user_id'])
            print('user', user)
            if not user.isEmailVerified:
                user.isEmailVerified = True
                user.is_active = True
                user.save()
            
            context = {
                'username': user.username,
                'user_email': user.email
            }

            return render(request, "picastro_web/verify_email.html", context=context)
        except jwt.ExpiredSignatureError as identifier:
            return Response(
                {'error': 'Activation link expired'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except jwt.exceptions.DecodeError as identifier:
            return Response(
                {'error': 'Invalid token'},
                status=status.HTTP_400_BAD_REQUEST
            )


class Payment(LoginRequiredMixin, TemplateView):
    template_name = 'picastro_web/pay_subscription.html'

    def post(self, request):
        user = request.user
        stripe.api_key = settings.STRIPE_SECRET_KEY

        checkout_session = stripe.checkout.Session.create(
            line_items=[{"price": "price_1OKVKdKVqvas7Ujje2cYbnD5", "quantity": 1}],
            mode="payment",
            customer_creation = 'always',
            success_url = settings.DOMAIN + reverse_lazy('payment_successful'),
            cancel_url = settings.DOMAIN + reverse_lazy('payment_failed'),
            customer_email = user.email
        )
        return redirect(checkout_session.url, code=303)


class PaymentPending(TemplateView):
    template_name = 'picastro_web/payment_pending.html'


class PaymentSuccessful(UserPassesTestMixin, TemplateView):
    template_name = 'picastro_web/payment_successful.html'

    def test_func(self):
        return self.request.user.subscriptionExpiry > datetime.now(timezone.utc)

    def handle_no_permission(self):
        return redirect(reverse('pay_subscription'))


class PaymentFailed(TemplateView):
    template_name = 'picastro_web/payment_failed.html'


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = settings.DOMAIN
        stripe.api_key = settings.STRIPE_SECRET_KEY
        print(request.user.id)
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                # client_reference_id=request.user.id if request.user.is_authenticated else None,
                success_url=domain_url + reverse_lazy('payment_successful') + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + reverse_lazy('payment_failed'),
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'price': 'price_1OKVKdKVqvas7Ujje2cYbnD5',
                        'quantity': 1,
                    }
                ],
            
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # Fetch all the required data from session
        client_reference_id = session.get('client_reference_id')
        stripe_customer_id = session.get('customer')
        stripe_subscription_id = session.get('subscription')
        stripe_customer_email = session.get('customer_email')

        # Get the user and create a new StripeCustomer
        user = PicastroUser.objects.get(email=stripe_customer_email)
        print(user.username + stripe_customer_email + ' just subscribed.')

        print("stripe_webhook user", user.username)
        user.subscriptionExpiry += timedelta(days=365)

        session_id = session.get('id', None)
        #time.sleep(15)
        user.payment_checkout_id = session_id

        user.save()
        return render(request, "picastro_web/payment_successful.html")
    return HttpResponse(status=200)
