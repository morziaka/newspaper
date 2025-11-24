from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.models import User

from .models import Post


@shared_task
def subscribers_notification_task(**params):
    send_mail(**params)

@shared_task
def subscribers_notification_weekly():
    before_datetime = timezone.now() - timedelta(days=7)
    posts = Post.objects.filter(time_post__gte=before_datetime)
    subscribers = User.objects.all()
    for subscriber in subscribers:
        text = ''
        for post in posts:
            post_categories = post.categories.all()
            text = ''
            for category in post_categories:
                if subscriber.email and category in subscriber.categories.all():
                    queryset = posts.filter(categories=category).values("title", "id")
                    for query in queryset:
                        if str(query["title"]) not in text:
                            text = text + f'<a href = "{settings.SITE_URL}/posts/{int(query["id"])}">{str(query["title"])}</a> \n'
        if text != '':
            send_mail(
                subject=f'Новинки за неделю на Новостном портале',
                message=(
                    f'Привет, {subscriber.username}! Ознакомьтесь с новинками за неделю по вашим подпискам. \n'
                    f'Список статей: \n {text}'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[subscriber.email],
                fail_silently=True
            )