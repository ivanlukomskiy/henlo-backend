from django.apps import AppConfig


class FlipItAppConfig(AppConfig):
    name = 'flip_it_app'

    def ready(self):
        print("123456789")
