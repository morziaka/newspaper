from django import forms
from django.core.exceptions import ValidationError
from .models import Post

class PostForm(forms.ModelForm):
   class Meta:
       model = Post
       fields = ['author', 'categories', 'title', 'text_post', 'rating_post']
       labels = {
    'author' : 'Автор',
    'categories' : 'Категории',
    'title' : 'Название',
    'text_post' : 'Содержание',
    'rating_post' : 'Рейтинг'
       }