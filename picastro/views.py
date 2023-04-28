from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    GenericAPIView
)
from rest_framework import filters
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Post, UserProfile
from django_filters.rest_framework import DjangoFilterBackend

from picastro.serializers import (
    CreateUserSerializer,
    PostSerializer,
    UserSerializer,
    UserProfileSerializer,
    # ResetPasswordEmailRequestSerializer
) 


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


class UserProfileAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)
    queryset = UserProfile.objects.all()
    lookup_field = 'id'


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
    ordering = '-pub_date'

    def perform_create(self, serializer):
        return serializer.save(poster=self.request.user)


class PostDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    lookup_field = 'id'
