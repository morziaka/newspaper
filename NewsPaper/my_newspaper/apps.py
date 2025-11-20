from django.apps import AppConfig


class MyNewspaperConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'my_newspaper'

    def ready(self):
        import my_newspaper.signals
