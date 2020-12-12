from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
import datetime
# from django.contrib.auth.models import User
from .forms import SignUpForm, ProfileForm
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from .utils import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.apps import apps

from .models import Customer

# from django.views.generic import DetailView
from django.views.generic import TemplateView, ListView

from django.contrib.auth.models import User
import json


connection = apps.get_app_config('car').connection

start_date = datetime.now()
end_date = datetime.now() + timedelta(days=1)
location = ''
location2 = ''
car_rent = []
car_info = []


def home(request):
    if request.method == 'GET':
        location_list = get_office_locations(connection)

    return render(request, 'car/home.html', {"my_locations": location_list, "dates": get_dates()})


def about(request):
    return render(request, 'car/about.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            print(form.cleaned_data)
            return redirect('/')
    else:
        form = SignUpForm()
        print(type(request.user))
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'car/signup.html', {'form': form,'profile_form': profile_form})


def search(request):
    global start_date, end_date
    global location, location2
    location = request.GET['location']
    location2 = request.GET['location2']
    start_date = request.GET['start']
    end_date = request.GET['end']
    cars = get_available_cars(connection, location, 'all')
    location = get_location_info(connection, location)
    location2 = get_location_info(connection, location2)
    print(cars)
    
    start_date = start_date.split(' ', 1 )[0]
    end_date = end_date.split(' ', 1 )[0]
    #print(start_date)
    #print(end_date)

    return render(request, 'car/search.html', {"cars": cars})


@login_required(login_url='/login/')
def booking(request):
    global car_rent, car_info
    car = request.GET['BOOK']
    if request.user.is_authenticated:
        car_info = get_car_info(connection, car)

    if 'type_id' in car_info[0]:
        car_rent = get_car_class_info(connection, car_info[0]['type_id'])
    current_user = request.user
    print(car_info)
    print(type(car_rent[0]['rent_charge']))
        
    return render(request, 'car/new_booking.html', {"car": car_info, "user":current_user,"dates": get_dates(),"rent":car_rent , "start_date":start_date,"end_date":end_date,"location":location,"location2":location2}  )
        

def invoices(request):

    coupon = request.GET['coupon']
    coupon_amount = get_coupon_info(connection, coupon)
    print(coupon_amount)
    current_user = request.user
    total_amount = calculate_total(start_date, end_date,coupon_amount[0]['discount'],car_rent[0]['rent_charge'])
    return render(request, 'car/invoices.html', {"car": car_info,"user":current_user,"dates": get_dates(),"rent":car_rent ,"coupon":coupon_amount,"start_date":start_date,"end_date":end_date,"total_amount":total_amount,})


