from asyncio.windows_events import NULL
from http.client import HTTPResponse
from multiprocessing import AuthenticationError
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login

from .forms import AddCommentForm, AddPostForm, EditProfileForm, LoginUserForm, RegisterUserForm
from .models import *

def index(request): 
    latest_posts_list = Post.objects.order_by('-post_date')[:10]

    return render(request, 'blog/list.html', {'latest_posts_list': latest_posts_list})

def profile(request, profile_id):
    latest_posts_list = Post.objects.filter(profile_id=profile_id)
    latest_posts_list = latest_posts_list.order_by('-post_date')
    profile = Profile.objects.get(user_id=profile_id)
    profile.posts = latest_posts_list.__len__
    title = profile.user.username
    content = {
        'latest_posts_list': latest_posts_list,
        'profile': profile,
        'title': title,
    }

    return render(request, 'blog/profile.html', {'content':content})


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Page not found: error 404</h1>')

def addPost(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.profile_id = request.user.id
            instance.save()
            _r = str(request.user.id)
            return redirect('profile/' + _r)
    else:
        form = AddPostForm()
    return render(request, 'blog/addpost.html', {'form': form})

def addComment(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.profile_id = request.user.id
            instance.post_id = post_id
            instance.save()
            _r = str(post_id)
            return redirect(reverse('show_post', kwargs={'post_id': post_id}))
    else:
        form = AddCommentForm()

    content = {
        'form': form,
        'post': post
    }
    return render(request, 'blog/addcomment.html', {'content': content})

def showPost(request, post_id):
    post = Post.objects.get(id=post_id)
    title = post.profile.user.username + "  " + str(post.post_date)
    comments = Comment.objects.filter(post_id=post_id)
    content = {
        'post': post,
        'title': title,
        'comments': comments
    }
    return render(request, 'blog/post.html', {'content':content})

def EditProfile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            _r = str(request.user.id)
            return redirect('profile/' + _r)
    else:
        form = EditProfileForm(instance=profile)
    return render(request, 'blog/editprofile.html', {'form': form})

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'blog/register.html'
    success_url = reverse_lazy('login')
    
    def get_context_data(self, *, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('edit_profile')

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'blog/login.html'

    def get_context_data(self, *, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))
    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')



