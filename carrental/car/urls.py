from django.urls import path
from car import views
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from car.views import CarDetailsView
from car.views import NewBookingView
from car.views import HomeView


urlpatterns = [
    path('', views.home,name="home"),
    path('about/',views.about,name="about"),
  
    path('loggin/',views.loggin,name="loggin"),
    path('signUp/',views.signUp,name="signUp"),
    path('carlist/<int:id>',views.search,name="carlist"),

    url(r'^$', HomeView.as_view(), name='homes'),
    
    url(r'^car/(?P<pk>\d+)/$', CarDetailsView.as_view(), name='car_details'),

    url(r'^booking/(?P<car_pk>\d+)/$', NewBookingView.as_view(), name='new_booking'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)