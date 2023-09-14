from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    DestroyAPIView,
    GenericAPIView
)
from rest_framework import filters
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from .models import Post, UserProfile, SavedImages
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.mixins import UserPassesTestMixin

from picastro.serializers import (
    CreateUserSerializer,
    PostSerializer,
    UserSerializer,
    UserProfileSerializer,
    LikeImageSerializer,
    CommentSerializer,
    # ResetPasswordEmailRequestSerializer
)
from django.http import JsonResponse
from .models import Post, Comment, UserProfile, SavedImages
from django.views.generic import ListView
from django_filters.rest_framework import DjangoFilterBackend


class CreateUserAPIView(CreateAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # We create a token than will be used for future auth

        return Response(
            {**serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class VerifyEmail(GenericAPIView):
    def get(self):
        pass


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


class HomePageView(ListView):
    model = Post
    template_name = "home.html"


class UserProfileAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)
    queryset = UserProfile.objects.all()
    lookup_field = 'user_id'


class RequestPasswordResetEmail(GenericAPIView):
    pass


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
        
        self.queryset = self.queryset.order_by(ordering)
        print(ordering)
        return self.queryset

    def perform_create(self, serializer):
        return serializer.save(poster=self.request.user)


class PostRandomAPIView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all().order_by('?')


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
        self.queryset = self.queryset.filter(user=self.request.user)
        return self.queryset
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        request.data['post'] = self.kwargs['post']
        request.data['user'] = request.user.id
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
        user = self.get_user(request)
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


class CommentListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer

    queryset = Comment.objects.all()
    lookup_field = 'post'


class CommentUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    lookup_field = 'id'
