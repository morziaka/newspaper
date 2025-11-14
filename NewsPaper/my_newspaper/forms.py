from django import forms
from django.core.exceptions import ValidationError
from .models import Post

class PostForm(forms.ModelForm):
   class Meta:
       model = Post
       fields = ['categories', 'title', 'text_post']
       labels = {
    'categories' : 'Категории',
    'title' : 'Название',
    'text_post' : 'Содержание',

       }