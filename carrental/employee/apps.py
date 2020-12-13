from django.apps import AppConfig
from .utils import create_connection


class EmployeeConfig(AppConfig):
    name = 'employee'
