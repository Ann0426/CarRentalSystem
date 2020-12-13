from django.urls import path

from .views import employeeHome,UpdateCar
urlpatterns = [
    path('',employeeHome , name="employeeHome" ),
    path('UpdateCar/',UpdateCar , name="UpdateCar" )]