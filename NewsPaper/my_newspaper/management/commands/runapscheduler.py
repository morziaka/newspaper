import logging
from datetime import timedelta

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from django.core.mail import send_mail

from my_newspaper.models import Post, Category

logger = logging.getLogger(__name__)


def weekly_mailing():
    before_datetime = timezone.now() - timedelta(days=7)
    posts = Post.objects.filter(time_post__gte=before_datetime)
    subscribers = User.objects.all()
    for subscriber in subscribers:
        text = ''
        for post in posts:
            post_categories = post.categories.all()
            for category in post_categories:
                if subscriber.email and category in subscriber.categories.all():
                    queryset = posts.filter(categories = category).values("title", "id")
                    for query in queryset:
                        if str(query["title"]) not in text:
                            text = text + f'<a href = "{settings.SITE_URL}/posts/{int(query["id"])}">{str(query["title"])}</a> \n'
        if text != '':
            send_mail(
                subject=f'Новинки за неделю на Новостном портале',
                message= (
                    f'Привет, {subscriber.username}! Ознакомьтесь с новинками за неделю по вашим подпискам. \n'
                    f'Список статей: \n {text}'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[subscriber.email],
                fail_silently=True
            )


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            weekly_mailing,
            trigger=CronTrigger(second="*/30"),
            id = "weekly_mailing",
            max_instances = 1,
            replace_existing = True,
        )
        logger.info("Added job 'weekly_mailing'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")