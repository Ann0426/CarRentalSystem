from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
import datetime
# from django.contrib.auth.models import User

from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from .utils import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.apps import apps


# from django.views.generic import DetailView
from django.views.generic import TemplateView, ListView

from django.contrib.auth.models import User
import json


connection = apps.get_app_config('car').connection
# Create your views here.

@login_required(login_url='/login/')
def employee_home(request):
    if not request.user.is_superuser:
        return HttpResponse("You do not have permissions to access this")
    location_list = get_office_locations(connection)
    types = get_car_class_info(connection)
    return render(request, 'car/employeeUpdateCar.html',{"my_locations": location_list, "dates": get_dates(), 'types':types})


@login_required(login_url='/login/')
def update_car(request):
    if not request.user.is_superuser:
        return HttpResponse("You do not have permissions to access this")

    updatelocation = request.GET['updatelocation']
    vehicle_id = get_vehicle_id(connection) + 1
    vehicle_model = request.GET['vehicle_model']
    vehicle_make = request.GET['vehicle_make']
    vehicle_vin = request.GET['vehicle_vin']
    vehicle_year = request.GET['vehicle_year']
    vehicle_license_plate_no = request.GET['vehicle_license_plate_no']
    vehicle_type = request.GET['vehicle_type']
    date = get_dates()['today']
    print("updatelocation",updatelocation)
    print("vehicle_id" ,vehicle_id)
    print("vehicle_model",vehicle_model)
    print("vehicle_make",vehicle_make)
    print("vehicle_vin",vehicle_vin)
    print("vehicle_year",vehicle_year)
    print("vehicle_license_plate_no",vehicle_license_plate_no)
    print("date", date)
    
    
    create_car(connection, updatelocation, vehicle_id, vehicle_model ,vehicle_make,vehicle_vin,vehicle_year,vehicle_license_plate_no, vehicle_type)

    location_list = get_office_locations(connection)
    types = get_car_class_info(connection)

    return render(request, 'car/employeeUpdateCar.html',{"my_locations": location_list, "dates": get_dates(), 'types':types})
