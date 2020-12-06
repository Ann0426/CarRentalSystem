from django.urls import path
from car import views
from django.conf import settings
from django.conf.urls import url

from django.conf.urls.static import static
from .views import search, home, about, signup, booking, invoices
# from car.views import CarDetailsView
# from car.views import NewBookingView
# from car.views import HomeView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', home, name="home" ),
    path('about/', about, name="about"),
    path('login/', auth_views.LoginView.as_view(template_name="car/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name="car/logout.html"), name='logout'),
    path('search/', search, name='search_results'),
    path('booking/', booking, name='new_booking'),
    path('invoices/', invoices, name='invoices'),
    # path('logout/$', auth_views.LogoutView(template_name="logged_out.html"), name='logout'),
    # path('^logout/$', auth_views.LogoutView, {'next_page': 'car/home.html'}, name='logout'),
    path('signUp/', signup, name="signUp")]

         # url(r'^$', HomeView.as_view(), name='homes'),
    
    # url(r'^car/(?P<pk>\d+)/$', CarDetailsView.as_view(), name='car_details'),

    # url(r'^booking/(?P<car_pk>\d+)/$', NewBookingView.as_view(), name='new_booking'),
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)]