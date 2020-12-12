from django.apps import AppConfig
from .utils import create_connection


class EmployeeConfig(AppConfig):
    name = 'employee'

    def __init__(self, app_name, app_module):
        super(EmployeeConfig, self).__init__(app_name, app_module)
        self.connection = None

    def ready(self):
        self.connection = create_connection()
