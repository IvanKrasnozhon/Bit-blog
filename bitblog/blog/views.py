from http.client import HTTPResponse
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from .models import Post, Comment, Profile

def index(request): 
    latest_posts_list = Post.objects.order_by('-post_date')[:10]
    return render(request, 'blog/list.html', {'latest_posts_list': latest_posts_list})
