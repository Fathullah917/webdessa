# myapp/apps.py (INI YANG BENAR DAN DISARANKAN)
from django.apps import AppConfig


class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'