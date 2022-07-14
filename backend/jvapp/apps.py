from django.apps import AppConfig


class JvappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jvapp'
    
    def ready(self):
        from . import signals
