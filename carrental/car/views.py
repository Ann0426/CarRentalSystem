from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
import datetime
# from django.contrib.auth.models import User
from car.signinform import SignUpForm

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from car.utils import get_office_locations, create_connection

# from django.views.generic import CreateView
# from django.views.generic import DetailView
from django.views.generic import TemplateView, ListView
# from car.models import Booking
# from car.models import Car
from car.models import City
from django.db.models import Q 

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
    if request.method == 'GET':
        location_list =  get_office_locations(create_connection())
        office_list = [i['city']+', '+i['address'] for i in location_list]
    
    return render(request,'car/home.html',{"my_locations":office_list})

    
       
       

def about(request):
    return render(request,'car/about.html')


def signUp(request):
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
class SearchResultsView(ListView):
    model = City
    template_name = 'car/search_results.html'
    # location_list =  get_office_locations(create_connection())
    # office_list = [i['city']+', '+i['address'] for i in location_list]

    def get_queryset(self): # new
        
        query = self.request.GET.get('q')
        print(query)
        if not query: query = ''
        object_list = City.objects.filter(
            Q(name__icontains=query) | Q(state__icontains=query)
        )
        print(object_list)
        return object_list
 
    
    # def showlocations(self, req):
    #     location_list =  get_office_locations(create_connection())
    #     office_list = [i['city']+', '+i['address'] for i in location_list]
    #     return render(req,'home.html', office_list)
    

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
