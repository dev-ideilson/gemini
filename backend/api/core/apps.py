from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.core'

    def ready(self):
        import api.core.handlers as handlers
        handlers.auto_register_handlers()