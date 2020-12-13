from django.urls import path
from django.contrib.auth import views as auth_views


from .views import employee_home,update_car
urlpatterns = [
    path('', employee_home, name="employeeHome" ),
    path('updatecar/', update_car, name="UpdateCar" ),
    path('corporateadd/', employee_home, name="corpadd"),
    path('corpcustadd/', employee_home, name="corpcustadd"),
    path('rentaltakeout/', employee_home, name="rentaltakeout"),
    path('login/', auth_views.LoginView.as_view(template_name="car/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name="car/logout.html"), name='logout'),
]