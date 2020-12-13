from django.urls import path

from .views import employeeHome,UpdateCar
urlpatterns = [
    path('', employeeHome , name="employeeHome" ),
    path('updatecar/', UpdateCar , name="UpdateCar" ),
    path('corporateadd', employeeHome),
    path('corpcustadd', employeeHome),
    path('rentaltakeout', employeeHome)
]