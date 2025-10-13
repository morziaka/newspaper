from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Author(models.Model):
    rating_user = models.IntegerField(default=0)
    usr = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        post_list = Post.objects.filter(author = self.id).all()
        rating_list = [post.rating_post for post in post_list]
        post_id = [post.id for post in post_list]
        comm_list = Comment.objects.filter(post_user_id = self.id).all()
        rating_list1 = [comm.rating_comm for comm in comm_list]
        comm_list1 = Comment.objects.all()
        comm_id = [com.post_comment_id for com in comm_list1]
        for id in comm_id:
            if id in post_id:
                rating_list2 = [comm.rating_comm for comm in comm_list1]

        self.rating_user = sum(rating_list)*3 + sum(rating_list1) + sum(rating_list2)
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=100, unique = True)

class Post(models.Model):
    news = 'NW'
    articles = "AR"
    types =((news, 'Новости'), (articles, 'Статьи'))
    time_post = models.DateTimeField(auto_now_add=True)
    post_types = models.CharField(max_length=2, choices = types, default = news)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length = 100)
    text_post = models.TextField()
    rating_post = models.IntegerField(default = 0)

    def like(self):
        self.rating_post = self.rating_post + 1
        self.save()

    def dislike(self):
        self.rating_post = self.rating_post - 1
        self.save()

    def Preview(self):
        if len(self.text_post) <= 124:
            return self.text_post
        else:
            return self.text_post[0:123] + '...'


class PostCategory(models.Model):
    posts = models.ForeignKey(Post, on_delete=models.CASCADE)
    postcat = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post_comment = models.ForeignKey(Post, on_delete=models.CASCADE)
    post_user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comm = models.TextField()
    time_comm = models.DateTimeField(auto_now_add=True)
    rating_comm = models.IntegerField(default=0)

    def like(self):
        self.rating_comm = self.rating_comm + 1
        self.save()

    def dislike(self):
        self.rating_comm = self.rating_comm - 1
        self.save()









