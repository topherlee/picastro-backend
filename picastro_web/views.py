from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from picastro.models import Post
from .forms import LoginForm, PostForm, UserRegistrationForm


class HomePageView(LoginRequiredMixin, ListView):
    model = Post
    ordering_fields = ['id', 'imageCategory', 'pub_date', 'poster']
    ordering = '-pub_date'
    template_name = "picastro_web/home.html"


class DashboardView(LoginRequiredMixin, ListView):
    model = Post
    ordering_fields = ['id', 'imageCategory', 'pub_date', 'poster']
    ordering = '-pub_date'
    template_name = "picastro_web/dashboard.html"

    
    def get_queryset(self):
        print(self.request.user)
        return Post.objects.filter(poster__username__contains=self.request.user)


class CreatePostView(LoginRequiredMixin, CreateView):  # new
    model = Post
    form_class = PostForm
    template_name = "picastro_web/post.html"
    success_url = reverse_lazy("dashboard")


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
    return render(request, 'picastro_web/login.html', {'form': form})
