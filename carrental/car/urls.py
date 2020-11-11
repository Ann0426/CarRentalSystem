from django.urls import path
from car import views

urlpatterns = [
    path('', views.home,name="home"),
    path('about/',views.about,name="about"),
  
    path('loggin/',views.loggin,name="loggin"),
    path('signUp/',views.signUp,name="signUp"),
    path('carlist/<int:id>',views.search,name="carlist"),
    
   
    
]