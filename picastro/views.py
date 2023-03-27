from django.shortcuts import render

# Create your views here.
from django.contrib.auth import get_user_model
from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
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
from picastro.serializers import (
    CreateUserSerializer,
    PostSerializer,
    UserSerializer,
    UserProfileSerializer,
) 
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .models import Post, UserProfile
from django.views.generic import ListView
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, PostForm
from django.contrib.auth.decorators import login_required

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


@api_view(['GET', 'POST', 'DELETE'])       #old API, delete later on
def get_post_list(request):
    if request.method == "GET":
        rest_list = Post.objects.order_by('-pub_date')
        serializer = PostSerializer(rest_list, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)


class HomePageView(ListView):
    model = Post
    template_name = "home.html"


class PostViewSet(ModelViewSet):    #old API, delete later on
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer


#new setup for Post API endpoint to do all together:
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
    

    def perform_create(self, serializer):
        return serializer.save(poster = self.request.user)


class PostDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    lookup_field = 'id'


class UserProfileAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)
    queryset = UserProfile.objects.all()
    lookup_field = 'id'


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'picastro/login.html', {'form': form})

def dashboard(request):
    return render(request,
                  'picastro/dashboard.html',
                  {'section': 'dashboard'}

    )

def post_image(request):
    form = PostForm()
    return render(request,
          'post.html',{'form' : form})

#def signup(request): 
    #form = SignUpForm(request.POST) 
    #if form.is_valid(): 
        #user = form.save()
         #user.refresh_from_db() 
         #user.first_name = form.cleaned_data.get('first_name') 
         #user.last_name = form.cleaned_data.get('last_name') 
         #address = form.cleaned_data.get('address') 
         #user.save() profile = Profile.objects.create(address=address, user_id=user.id) 
         #profile.save() 
         #username = form.cleaned_data.get('username') 
         #password = form.cleaned_data.get('password1') 
         #user = authenticate(username=username, password= password) 
         #login(request, user) 
         #return redirect('/') 
         #return render(request, 'registration/signup.html', {'form': form})
