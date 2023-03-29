from django.shortcuts import render

# Create your views here.
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from .models import Post, UserProfile
from django.views.generic import ListView, CreateView
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, PostForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
#from django.urls import reverse_lazy

class HomePageView(ListView):
    model = Post
    template_name = "home.html"
# Create your views here.
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
                          'picastro/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'picastro/register.html',
                  {'user_form': user_form})

# def post_image(request):
#     form = PostForm()
#     return render(request,
#           'post.html',{'form' : form})

class CreatePostView(CreateView):  # new
    model = Post
    form_class = PostForm
    template_name = "post.html"
    #success_url = reverse_lazy("home")