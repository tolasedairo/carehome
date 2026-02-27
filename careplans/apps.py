from django.apps import AppConfig


class CareplansConfig(AppConfig):
    name = 'careplans'

    def ready(self):
        import careplans.signals  # noqa: F401
