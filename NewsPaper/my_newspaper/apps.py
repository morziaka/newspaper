from django.apps import AppConfig
import redis


class MyNewspaperConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'my_newspaper'

    def ready(self):
        import my_newspaper.signals

red = redis.Redis(host = 'localhost', port = 6379)