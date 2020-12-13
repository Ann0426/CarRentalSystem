from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
import datetime
# from django.contrib.auth.models import User
from .forms import SignUpForm
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
        global connection
        if not connection.open:
            connection = create_connection()
        location_list = get_office_locations(connection)

    return render(request, 'car/home.html', {"my_locations": location_list, "dates": get_dates()})


def about(request):
    return render(request, 'car/about.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
       
        if form.is_valid() :
            form.save()
            
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            print(form.cleaned_data)
            return redirect('/')
    else:
        form = SignUpForm()
        
    return render(request, 'car/signup.html', {'form': form})


def search(request):
    global start_date, end_date
    global location, location2
    location = request.GET['location']
    location2 = request.GET['location2']
    start_date = request.GET['start']
    end_date = request.GET['end']
    request.session['location'] = location
    request.session['location2'] = location2
    global connection
    if not connection.open:
        connection = create_connection()
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
    global connection
    car = request.GET['BOOK']
    request.session['vehicle_id'] = car
    if request.user.is_authenticated:
        if not connection.open:
            connection = create_connection()
        car_info = get_car_info(connection, car)

    if not connection.open:
        connection = create_connection()
    car_rent = get_car_class_info(connection, car_info[0]['type_id'])
    car_info[0]['rent_charge'] = float(car_rent[0]['rent_charge'])
    request.session['vehicle_info'] = car_info[0]
    current_user = request.user
        
    return render(request, 'car/new_booking.html', {"car": car_info, "user":current_user,"dates": get_dates(),"rent":car_rent , "start_date":start_date,"end_date":end_date,"location":location,"location2":location2}  )
        

def invoices(request):

    coupon = request.GET['coupon']
    global connection
    if not connection.open:
        connection = create_connection()
    coupon_amount = get_coupon_info(connection, coupon)
    print(coupon_amount)
    current_user = request.user
    total_amount = calculate_total(start_date, end_date,coupon_amount[0]['discount'],car_rent[0]['rent_charge'])
    if coupon == "":
        coupon = "null"
    request.session['coupon'] = coupon
    invoice_id = get_invoice_id(connection) + 1
    #invoice_id = result + 1
    create_invoice(connection, invoice_id, end_date, total_amount)
    info = {
        'rental_id': generate_rental_id(connection) + 1,
        #'rental_id': 1,
        'invoice_id': invoice_id,
        'pickup_date': start_date,
        'dropoff_date': end_date,
        'coupon_id': coupon,
        'vehicle_id': car_info[0]['vehicle_id'],
        'cust_id': 1,
        'pickup_office': int(location[0]['offices_id']),
        'dropoff_office': int(location2[0]['offices_id']),
    }
    print(info)
    create_rental(connection, info)
    return render(request, 'car/invoices.html', {"car": car_info,"user":current_user,"dates": get_dates(),"rent":car_rent ,"coupon":coupon_amount,"start_date":start_date,"end_date":end_date,"total_amount":total_amount,})


def make_payment(request):
    print(request.session.items())
    return render(request, 'car/about.html')