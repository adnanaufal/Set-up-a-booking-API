from django.shortcuts import render
from .forms import BookingForm
from .models import Menu
from django.core import serializers
from .models import Booking
from datetime import datetime
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


# Create your views here.
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def reservations(request):
    date = request.GET.get('date',datetime.today().date())
    bookings = Booking.objects.all()
    booking_json = serializers.serialize('json', bookings)
    return render(request, 'bookings.html',{"bookings":booking_json})

def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'book.html', context)

# Add your code here to create new views
def menu(request):
    menu_data = Menu.objects.all()
    main_data = {"menu": menu_data}
    return render(request, 'menu.html', {"menu": main_data})


def display_menu_item(request, pk=None): 
    if pk: 
        menu_item = Menu.objects.get(pk=pk) 
    else: 
        menu_item = "" 
    return render(request, 'menu_item.html', {"menu_item": menu_item}) 

@csrf_exempt
def bookings(request):
    if request.method == "POST":
        data = json.load(request)  # Assuming it's working for your tutorial's context
        exist = Booking.objects.filter(reservation_date=data['reservation_date']).filter(reservation_slot=data['reservation_slot']).exists()
        
        if not exist:
            # If no conflict, create and save the booking
            booking = Booking(
                first_name=data['first_name'],
                reservation_date=data['reservation_date'],
                reservation_slot=data['reservation_slot'],
            )
            booking.save()
        else:
            # If the booking already exists, return an error message in JSON
            return HttpResponse("{\"error\":1}", content_type='application/json')

    
    # date = request.GET.get('date', datetime.today().date())
    # Handle GET request to fetch bookings for a particular date
    date_str = request.GET.get('date', str(datetime.today().date()))  # Default to today's date if no date is passed
    try:
        # Try parsing the date from the query parameter
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        # If invalid date format, fall back to today's date
        date = datetime.today().date()

    bookings = Booking.objects.filter(reservation_date=date)
    booking_json = serializers.serialize('json', bookings)
    
    return HttpResponse(booking_json, content_type='application/json')