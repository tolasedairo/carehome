from django.apps import AppConfig


class HandoversConfig(AppConfig):
    name = 'handovers'

    def ready(self):
        import handovers.signals  # noqa: F401
