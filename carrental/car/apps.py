from __future__ import unicode_literals
from django.apps import AppConfig
from .utils import create_connection

class CarConfig(AppConfig):
    name = 'car'

    def __init__(self, app_name, app_module):
        super(CarConfig, self).__init__(app_name, app_module)
        self.connection = None

    def ready(self):
        self.connection = create_connection()
