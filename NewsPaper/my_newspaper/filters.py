import django_filters
from django import forms
from django_filters import FilterSet, CharFilter, ModelChoiceFilter
from .models import Post, Author


class PostFilter(FilterSet):
   time_post_gt = django_filters.DateTimeFilter(field_name='time_post', lookup_expr='gt', label = 'Дата публикации позже, чем' )
   time_post_gt.field.widget = forms.DateInput(attrs={'type': 'date'})
   title = CharFilter(label = "Заголовок", lookup_expr='iregex')
   author = ModelChoiceFilter(queryset = Author.objects.all(), label = "Автор", empty_label= "Все авторы" )

   class Meta:
       model = Post
       fields = ['title', 'author', 'time_post_gt']


