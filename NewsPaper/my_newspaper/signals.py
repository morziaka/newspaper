from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import m2m_changed, pre_save, post_save
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from .tasks import subscribers_notification_task

from .models import Category, Post, PostCategory

@receiver(pre_save, sender = Post)
def post_limit_notification(sender, instance, *args, **kwargs):
    if instance.pk:
        return
    before_datetime = timezone.now() - timedelta(days=1)
    posts_count = Post.objects.filter(author = instance.author, time_post__gte=before_datetime).count()
    if posts_count >=3:
        raise PermissionDenied('Вы не можете размещать более 3 постов в сутки')

@receiver(m2m_changed, sender = PostCategory)
def newpost_notification(sender, instance, action, **kwargs):
    if action == 'post_add':
        current_categories = instance.categories.all()
        emails = []
        for category in current_categories:
            subscribers = category.subscribers.all()
            for user in subscribers:
                if user.email and user.email not in emails:
                    html_content = (
                        f'<p>Привет, {user.username}! На Новостном портале новая публикация "{instance.title}" в категориях: {", ".join(cat.name for cat in instance.categories.all())}. </p>'
                        f'<p>Краткое содержание: {instance.Preview()}</p>'
                        f'<p>Полный текст публикации <a href = "{settings.SITE_URL}/posts/{instance.id}">по этой ссылке</a></p>'
                    )
                    params = {
                        'subject': 'Новая публикация на Новостном портале',
                        'message':
                        f'Привет, {user.username}! На Новостном портале новая публикация "{instance.title}" в категориях: {", ".join(cat.name for cat in instance.categories.all())}. \n'
                        f'Краткое содержание: {instance.Preview()}.'
                        f'Полный текст публикации <a href = "{settings.SITE_URL}/posts/{instance.id}">по этой ссылке</a>',
                        'html_message' : html_content,
                        'from_email': settings.DEFAULT_FROM_EMAIL,
                        'recipient_list' : [user.email],
                        'fail_silently' : True
                    }
                    emails.append(user.email)
                    subscribers_notification_task.delay(**params)


@receiver(m2m_changed, sender = Category.subscribers.through)
def subscribers_notification(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        user = User.objects.get(pk__in=pk_set)
        send_mail(
            subject='Новая подписка',
            message=(
                f'Привет, {user.username}! Вы подписались на категорию {instance.name}. '
                f'Ваши текущие подписки: {", ".join(cat.name for cat in user.categories.all())}'
                ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True
        )

    if action == 'post_remove':
        user = User.objects.get(pk__in=pk_set)
        send_mail(
            subject='Отписка от категории',
            message=(
                f'Привет, {user.username}! Вы отписались от категории {instance.name}. '
                f'Ваши текущие подписки: {", ".join(cat.name for cat in user.categories.all())}'
                ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True
        )