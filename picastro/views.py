import os
import jwt

from rest_framework import filters
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    DestroyAPIView,
    GenericAPIView
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.encoding import (
    smart_str,
    force_str,
    smart_bytes,
    DjangoUnicodeDecodeError
)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import ListView, CreateView
from django_filters.rest_framework import DjangoFilterBackend

from picastro.serializers import (
    CreateUserSerializer,
    PostSerializer,
    UserSerializer,
    UserProfileSerializer,
    ResetPasswordEmailRequestSerializer,
    LikeImageSerializer,
    CommentSerializer,
    # ResetPasswordEmailRequestSerializer
)
from .models import PicastroUser, Post, Comment, SavedImages
from .utils import Util


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

        username = serializer.data['username']
        user_email = serializer.data['email']

        Util.send_token_email(relative_link, token, username, user_email)

        # absolute_Url = domain + relative_link + '?token='+token

        # email_body = 'Hi ' + username + \
        #     ',\nUse link below to verify your email address for Picastro: \n' + absolute_Url
        # data = {
        #     'email_subject': 'Verify your email for Picastro',
        #     'email_body': email_body,
        #     'user_email_address': user_email
        # }

        # print("body", email_body)
        # print("email data", data)

        # send_mail(
        #     'Verify your email for Picastro',
        #     email_body,
        #     settings.EMAIL_HOST_USER,
        #     [user_email],
        #     fail_silently=False,
        # )
        # Util.send_email(data)

        return Response(
            {**serializer.data},
            status=status.HTTP_201_CREATED
        )


# class VerifyEmail(GenericAPIView):
#     permission_classes = [AllowAny]
    
#     def get(self, request):
#         token = request.GET.get('token')
#         try:
#             payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
#             user = PicastroUser.objects.get(id=payload['user_id'])
#             print('user', user)
#             if not user.isEmailVerified:
#                 user.isEmailVerified = True
#                 # user.is_active = True
#                 user.save()

#             # return Response(
#             #     {'email': 'Successfully activated'},
#             #     status=status.HTTP_200_OK
#             # )
#             return redirect(reverse('pay_subscription'))
#         except jwt.ExpiredSignatureError as identifier:
#             return Response(
#                 {'error': 'Activation link expired'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         except jwt.exceptions.DecodeError as identifier:
#             return Response(
#                 {'error': 'Invalid token'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )


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
    queryset = PicastroUser.objects.all()
    lookup_field = 'id'


class RequestPasswordResetEmail(GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data['email']

        if PicastroUser.objects.filter(email=email).exists():
            user = PicastroUser.objects.filter(email=email)
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
                settings.EMAIL_HOST_USER,
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
    
    def get_queryset(self):
        order = self.request.GET.get("order")
        #print(order)
        if order == "random":
            ordering = "?"
        else:
            ordering = "-pub_date"
        
        requesting_user = self.request.user.id
        
        self.queryset = self.queryset.order_by(ordering)
        print(ordering)
        return self.queryset

    def perform_create(self, serializer):
        return serializer.save(poster=self.request.user)


class PostDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    lookup_field = 'id'


class ImageLikeAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LikeImageSerializer
    queryset = SavedImages.objects.all()

    def get_queryset(self):
        # list_of_liked_posts = self.queryset.filter(user=self.request.user)
        # values_of_liked_posts = list_of_liked_posts.values("post")
        # print(list_of_liked_posts)
        # print("values", values_of_liked_posts)
        # list_of_post_ids = []
        # for post in values_of_liked_posts:
        #     list_of_post_ids.append(post["post"])
        # list_new = []
        
        # print(list_of_post_ids)
        self.queryset = self.queryset.filter(user=self.request.user)
        return self.queryset
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        request.data['post'] = self.kwargs['post']
        request.data['user'] = Util.get_user(self, request)
        print("request.data", request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # We create a token than will be used for future auth

        return Response(
            {**serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers
        )
        
    # def test_func(self):
    #     post = self.kwargs['post']
    #     poster = Post.objects.filter(id=post).poster
    #     print("poster", poster)
    #     return not poster == self.request.user
    
    # def perform_create(self, serializer, *args, **kwargs):
    #     post = kwargs['post']
    #     print("post, user", post)
        
    #     return serializer.save(post=post)


class ImageDislikeAPIView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LikeImageSerializer
    queryset = SavedImages.objects.all()
    #lookup_field = 'unique_user_post_combination'

    def get_user(self, request, format=None):
        token_user_id = request.user.id
        print("token_user_id", token_user_id)
        
        return token_user_id
    
    # def test_func(self):
    #     poster = Post.objects.filter(id=post).poster
    #     print("poster", poster)
    #     return poster == self.request.user
    
    def destroy(self, request, *args, **kwargs):
        user = Util.get_user(self, request)
        print("kwargs", kwargs['post'])
        post = kwargs['post']
        instance = SavedImages.objects.filter(user=user, post=post)
        print("instance", instance)

        # original code of destroy() function of DestroyAPIView
        # Simply delete - no need to instantiate the serializer
        self.perform_destroy(instance)

        # Return an empty response
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer

    # def perform_create(self, serializer):
    #     print("serializer", serializer)
    #     serializer.save(commenter=self.request.user)


class CommentListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer
    ordering_fields = ['date_added']
    
    def get_queryset(self):
        return Comment.objects.filter(post__id=self.kwargs['post_id']).order_by('-date_added')


class CommentUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    lookup_field = 'id'
