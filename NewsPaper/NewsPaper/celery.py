import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
app.conf.update(
    CELERY_TIMEZONE = 'UTC',
    CELERY_POOL='solo',
)

app.conf.beat_schedule = {
    'weekly-mailing' : {
        'task': 'my_newspaper.tasks.subscribers_notification_weekly',
        'schedule': 30,

        }
}