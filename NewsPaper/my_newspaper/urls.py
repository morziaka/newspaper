from django.urls import path
# Импортируем созданное нами представление
from .views import *


urlpatterns = [
   path('', PostsList.as_view(), name = "post_list"),
   path('posts/', PostsList.as_view(), name = "post_list"),
   path('<int:pk>', PostDetail.as_view(), name = "post_detail"),
   path('news/create/', PostCreate.as_view(), name= "news_create"),
   path('search/', Search.as_view(), name= "search"),
   path('articles/create/', PostCreate.as_view(), name= "articles_create"),
   path('news/<int:pk>/edit/', PostUpdate.as_view(), name='news_update'),
   path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='articles_update'),
   path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
   path('articles/<int:pk>/delete/', PostDelete.as_view(), name='articles_delete'),
]