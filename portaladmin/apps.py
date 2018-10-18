from django.apps import AppConfig


class PortaladminConfig(AppConfig):
    name = 'portaladmin'

    def ready(self):
        from . import receivers