from django.apps import AppConfig


class loginConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'login'

class RegistrationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'registration'