from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
import datetime
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
    return render(request,'car/signup.html')
def loggin(request):
    return render(request,'car/login.html')
def search(request):
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