from django.shortcuts import render
from datetime import datetime
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post


class PostsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'posts'
    ordering = ['-time_post']

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


