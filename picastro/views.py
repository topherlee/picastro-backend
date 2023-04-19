from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    GenericAPIView
)
from rest_framework import filters
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import (
    smart_str,
    force_str,
    smart_bytes,
    DjangoUnicodeDecodeError
)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import send_mail

import os
import jwt

from django.http import JsonResponse
from .models import Post, UserProfile
from django.views.generic import ListView, CreateView
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse, reverse_lazy

from picastro.serializers import (
    CreateUserSerializer,
    PostSerializer,
    UserSerializer,
    UserProfileSerializer,
    ResetPasswordEmailRequestSerializer
)
from .utils import Util
from django.conf import settings


class CreateUserAPIView(CreateAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # We create a token than will be used for future auth
        print(serializer.data)
        #domain = 'http://13.42.37.75:8000'
        domain = 'http://127.0.0.1:8000'
        relative_link = reverse('email-verify')
        token = serializer.data['token']['access']
        print(token)

        absolute_Url = domain + relative_link + '?token='+token
        username = serializer.data['username']
        user_email = serializer.data['email']
        email_body = 'Hi ' + username + \
            ',\nUse link below to verify your email: \n' + absolute_Url
        data = {
            'email_subject': 'Verify your email for Picastro',
            'email_body': email_body,
            'user_email_address': user_email
        }

        print(os.environ.get('EMAIL_HOST_PASSWORD'))

        send_mail(
            'Verify your email for Picastro',
            email_body,
            'atzen78@web.de',
            [user_email],
            fail_silently=False,
        )
        # Util.send_email(data)
        return Response(
            {**serializer.data},
            status=status.HTTP_201_CREATED
        )


class VerifyEmail(GenericAPIView):
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user = UserProfile.objects.get(id=payload['user_id'])
            print('user', user)
            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response(
                {'email': 'Successfully activated'},
                status=status.HTTP_200_OK
            )
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


class LogoutUserAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CurrentUserView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserProfileAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)
    queryset = UserProfile.objects.all()
    lookup_field = 'id'


class RequestPasswordResetEmail(GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.filter(email=email)
            uidb64 = urlsafe_base64_encode(user.id)
            token = PasswordResetTokenGenerator().make_token(user)

            domain = 'http://13.42.37.75:8000/'
            # domain = 'http://127.0.0.1:8000/'
            relative_link = reverse(
                'password-reset-confirm', kwargs={'uibd64': uidb64, 'token': token})
            absolute_Url = domain + relative_link
            username = serializer.data['username']
            user_email = serializer.data['email']
            email_body = 'Hello,\nUse link below to reset your password: \n' + absolute_Url
            data = {
                'email_subject': 'Reset your password for Picastro',
                'email_body': email_body,
                'user_email_address': user_email
            }

            send_mail(
                'Verify your email for Picastro',
                email_body,
                'atzen78@web.de',
                [user_email],
                fail_silently=False,
            )

            return Response(
                {'success': 'We have sent you a link to reset your password'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'success': 'We could not find your email address. Please check again.'},
                status=status.HTTP_404_NOT_FOUND
            )


class PasswordTokenCheckAPI(GenericAPIView):
    def get(self, request, uidb64, token):
        pass


# @api_view(['GET', 'POST', 'DELETE'])       #old API, delete later on
# def get_post_list(request):
#     if request.method == "GET":
#         rest_list = Post.objects.order_by('-pub_date')
#         serializer = PostSerializer(rest_list, many=True, context={'request': request})
#         return JsonResponse(serializer.data, safe=False)


# class PostViewSet(ModelViewSet):    #old API, delete later on
#     permission_classes = (IsAuthenticated,)
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer


# new setup for Post API endpoint to do all together:
# post, retrieve, filter, search, update (for SortAndFilterScreen, HomeScreen, UserScreen)

class PostAPIView(ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter]
    filterset_fields = ['id', 'imageCategory', 'pub_date', 'poster']
    search_fields = ['astroNameShort', 'astroName']
    ordering_fields = ['id', 'imageCategory', 'pub_date', 'poster']
    ordering = '-pub_date'

    def perform_create(self, serializer):
        return serializer.save(poster=self.request.user)


class PostDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    lookup_field = 'id'
