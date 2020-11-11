from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
import datetime
from django.contrib.auth.models import User
from car.signinform import Signup
from car.loginform import Loggin
my_locations=[
        {"id":1,"name":"SF","no_of_car":4},
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
    
def home(request):
    return render(request,'car/home.html',{"my_locations":my_locations})

def about(request):
    return render(request,'car/about.html')
def signUp(request):
    form = Signup(request.POST or None)
    status= " "
    if form.is_valid():
        password= form.cleaned_data.get("password")
        confirm_password = form.cleaned_data.get("confirm_password")
        if(password!= confirm_password):
            status= "Your passwords don't match!"
        else:
            status= "Signup done successfully!"
    return render(request,'car/signup.html',{"form":form,"status":status})
def loggin(request):
    form = Loggin(request.POST or None)
    status= " "
    if form.is_valid():
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = next((user for user in users if user["email"] == email and user["password"] == password), None)
        if user:
            status="Successfully logged in!"
        else:
            status="Wrong Credentials!"
    return render(request,'car/login.html',{"form":form,"status":status})
def search(request,id):
    cars=[]
    location_name=''
    for carlist in my_locations:
        if(id == carlist['id']):
            location_name=carlist['name']

    # if len(location_name)==0:
    #     raise Http404("Such carlist does not exist")

    for car in rent_cars:
        if(id == car['my_locations_id']):
            cars.append(car)
    
    return render(request,'car/search.html',{"cars":cars,"location_name": location_name})