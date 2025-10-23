from datetime import datetime
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from .utils import *


class PostsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'posts'
    ordering = ['-time_post']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        path_create = reverse_lazy('news_create')
        return create_or_edit(context, self.request.path)

class Search(FilterView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'
    filterset_class = PostFilter
    ordering = ['-time_post']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create_or_update.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        path = self.request.path
        if 'articles' in str(path):
            post.post_types = 'AR'
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        path_create = reverse_lazy('news_create')
        return create_or_edit(context, self.request.path)



class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create_or_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        path_create = reverse_lazy('news_update')
        return create_or_edit(context, self.request.path)

class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return create_or_edit(context, self.request.path)

