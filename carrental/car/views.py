from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
import datetime
# from django.contrib.auth.models import User
from .signinform import SignUpForm

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .utils import get_office_locations
from django.apps import apps
from .utils import get_dates
from .utils import get_available_cars
# from django.views.generic import CreateView
# from django.views.generic import DetailView
from django.views.generic import TemplateView, ListView
# from car.models import Booking
# from car.models import Car
from .models import City
from django.db.models import Q 

my_locations=[
        {"id": 1,"name":"SF","no_of_car":4},
        {"id":2,"name":"LA","no_of_car":2}
    ]

rent_cars = [
            {"id": 1, "Model": "yaris", "Make": "toyota", "year": 20,"my_locations_id": 1},
            {"id": 2, "Model": "yaris", "Make": "toyota", "year": 20, "my_locations_id": 1},
            {"id": 3, "Model": "yaris", "Make": "toyota", "year":20, "my_locations_id": 1},
            {"id": 4, "Model": "yaris", "Make": "toyota", "year": 20, "my_locations_id": 1},
            {"id": 5, "Model": "yaris", "Make": "toyota", "year": 20,"my_locations_id": 2},
            {"id": 6, "Model": "yaris", "Make": "toyota", "year": 20, "my_locations_id": 2},
    ]
users = [
            {"id": 1, "full_name": "john", "email": "john123@gmail.com", "password": "adminpass"},
        ]

connection = apps.get_app_config('car').connection


def home(request):
    if request.method == 'GET':
        location_list = get_office_locations(connection)

    return render(request, 'car/home.html', {"my_locations": location_list, "dates": get_dates()})


def about(request):
    return render(request, 'car/about.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'car/signup.html', {'form': form})


def search(request):
    location = request.GET['location']
    cars = get_available_cars(connection, location, 'all')
    return render(request, 'car/search.html', {"cars": cars})


class SearchResultsView(ListView):
    model = City
    template_name = 'car/search_results.html'
    # location_list =  get_office_locations(create_connection())
    # office_list = [i['city']+', '+i['address'] for i in location_list]

    def get_queryset(self): # new
        
        query = self.request.GET.get('q')
        print(query)
        if not query:
            query = ''
        object_list = City.objects.filter(
            Q(name__icontains=query) | Q(state__icontains=query)
        )
        print(object_list)
        return object_list
 
    

############## refer to others
# class HomeView(TemplateView):
#     template_name = 'car/homes.html'

#     def get_context_data(self, **kwargs):
#         ctx = super(HomeView, self).get_context_data(**kwargs)

#         cars = Car.objects.filter(is_available=True)
#         ctx['cars'] = cars

#         return ctx


# class CarDetailsView(DetailView):
#     template_name = 'car/car_details.html'
#     model = Car

#     def get_context_data(self, **kwargs):
#         ctx = super(CarDetailsView, self).get_context_data(**kwargs)
#         ctx['booking_success'] = 'booking-success' in self.request.GET

#         return ctx


# class NewBookingView(CreateView):
#     model = Booking
#     fields = [
#         'customer_name', 'customer_email', 'customer_phone_number',
#         'booking_start_date', 'booking_end_date', 'booking_message'
#     ]

#     template_name = 'car/new_booking.html'

#     def get_car(self):
#         car_pk = self.kwargs['car_pk']
#         car = Car.objects.get(pk=car_pk)

#         return car

#     def get_context_data(self, **kwargs):
#         ctx = super(NewBookingView, self).get_context_data(**kwargs)
#         ctx['car'] = self.get_car()

#         return ctx

#     def form_valid(self, form):
#         new_booking = form.save(commit=False)
#         new_booking.car = self.get_car()
#         new_booking.is_approved = False

#         new_booking.save()

#         return super(NewBookingView, self).form_valid(form)

#     def get_success_url(self):
#         car = self.get_car()
#         car_details_page_url = car.get_absolute_url()

#         return '{}?booking-success=1'.format(car_details_page_url)
