from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
import datetime
# from django.contrib.auth.models import User
from .signinform import SignUpForm
import datetime

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .utils import get_office_locations
from django.apps import apps
from .utils import get_dates
from .utils import get_available_cars, get_car_info, get_car_class_info,get_coupon_info,get_location_info,calculate_total
# from django.views.generic import DetailView
from django.views.generic import TemplateView, ListView
# from car.models import Booking
# from car.models import Car
# from django.db.models import Q 
from django.contrib.auth.models import User


connection = apps.get_app_config('car').connection

start_date = ""
end_date = ""
car = []
location = []
location2 = []
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
    global start_date,end_date,location,location2
    location = request.GET['location']
    location2 = request.GET['location2']
    start_date = request.GET['Start']
    end_date = request.GET['end']
    cars = get_available_cars(connection, location, 'all')
    location = get_location_info(connection,location)
    location2 = get_location_info(connection,location2)
    print(cars)
    
    start_date = start_date.split(' ', 1 )[0] 
    end_date = end_date.split(' ', 1 )[0]
    print(start_date)
    print(end_date)
    print(type(start_date))

    return render(request, 'car/search.html', {"cars": cars})

def booking(request):
        global car,car_info,car_rent 
        car = request.GET['BOOK']
        if request.user.is_authenticated:
            car_info = get_car_info(connection,car)
        if 'type_id' in car_info[0]:
            car_rent = get_car_class_info(connection,car_info[0]['type_id'])
        current_user = request.user
        print(car_info)
        print(type(car_rent[0]['rent_charge']))
        
        return render(request, 'car/new_booking.html', {"car": car_info,"user":current_user,"dates": get_dates(),"rent":car_rent , "start_date":start_date,"end_date":end_date,"location":location,"location2":location2}  )
        

def invoices(request):
    coupon = request.GET['coupon']
    coupon_amount = get_coupon_info(connection,coupon)
    print(coupon_amount)
    current_user = request.user
    total_amount = calculate_total(start_date,end_date,coupon_amount[0]['discount'],car_rent[0]['rent_charge'])
    return render(request, 'car/invoices.html', {"car": car_info,"user":current_user,"dates": get_dates(),"rent":car_rent ,"coupon":coupon_amount,"start_date":start_date,"end_date":end_date,"total_amount":total_amount,})
    
 


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
