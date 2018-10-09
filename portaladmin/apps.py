from django.apps import AppConfig


class LoadReceivers(AppConfig):
    name = 'portaladmin'

    def ready(self):
        from . import receivers