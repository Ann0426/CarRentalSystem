from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
import datetime
# from django.contrib.auth.models import User
from car.signinform import Signup
from car.loginform import Loggin


from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import TemplateView

from car.models import Booking
from car.models import Car
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
users = [
            {"id": 1, "full_name": "john", "email": "john123@gmail.com", "password": "adminpass"},
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
############## refer to others
class HomeView(TemplateView):
    template_name = 'car/homes.html'

    def get_context_data(self, **kwargs):
        ctx = super(HomeView, self).get_context_data(**kwargs)

        cars = Car.objects.filter(is_available=True)
        ctx['cars'] = cars

        return ctx


class CarDetailsView(DetailView):
    template_name = 'car/car_details.html'
    model = Car

    def get_context_data(self, **kwargs):
        ctx = super(CarDetailsView, self).get_context_data(**kwargs)
        ctx['booking_success'] = 'booking-success' in self.request.GET

        return ctx


class NewBookingView(CreateView):
    model = Booking
    fields = [
        'customer_name', 'customer_email', 'customer_phone_number',
        'booking_start_date', 'booking_end_date', 'booking_message'
    ]

    template_name = 'car/new_booking.html'

    def get_car(self):
        car_pk = self.kwargs['car_pk']
        car = Car.objects.get(pk=car_pk)

        return car

    def get_context_data(self, **kwargs):
        ctx = super(NewBookingView, self).get_context_data(**kwargs)
        ctx['car'] = self.get_car()

        return ctx

    def form_valid(self, form):
        new_booking = form.save(commit=False)
        new_booking.car = self.get_car()
        new_booking.is_approved = False

        new_booking.save()

        return super(NewBookingView, self).form_valid(form)

    def get_success_url(self):
        car = self.get_car()
        car_details_page_url = car.get_absolute_url()

        return '{}?booking-success=1'.format(car_details_page_url)
