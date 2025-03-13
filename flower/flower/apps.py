from django.apps import AppConfig


class OrderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'order'

from django.conf import settings

class FlowerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'flower'

    def ready(self):
        if not settings.TESTING:
            from .del_telegram_bot import setup_bot
            setup_bot()