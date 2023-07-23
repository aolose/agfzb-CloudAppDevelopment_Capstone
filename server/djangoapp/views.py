from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

from .models import CarModel
from .restapis import get_dealers_from_cf, get_dealer_from_cf_by_id, \
    post_request, get_dealer_reviews_from_cf

# Get an instance of a logger
logger = logging.getLogger(__name__)
index = 'djangoapp/static_page.html'
endpoint = 'https://us-south.functions.appdomain.cloud.ivi.cx/api/v1/web/c224c6df-1c8f-4d73-980b-a78c0fdbe6b6/package/'
# endpoint = 'http://localhost:3000/'
ep_dealership = endpoint + 'dealer'
ep_review = endpoint + 'review'


# Create your views here.
def static_page_view(req):
    return render(req, 'djangoapp/static_page.html')


# Create an `about` view to render a static about page
# def about(request):
# ...


# Create a `contact` view to return a static contact page
# def contact(request):

# Create a `login_request` view to handle sign in request
# def login_request(request):
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            context = {"success": "login done!"}
    return redirect('djangoapp:index')


# ...

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')


# ...

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
def registration_request(request):
    context = {}
    if request.method == "POST":
        usr = request.POST['us']
        pwd = request.POST['pw']
        mail = request.POST['em']
        user = User.objects.create_user(usr, mail, pwd)
        user.save()
        context = {"success": usr + " created!"}
        return render(request, index, context)
    return render(request, 'djangoapp/registration.html', context)


# ...

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        dealerships = get_dealers_from_cf(ep_dealership)
        context["dealership_list"] = dealerships
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        context = {}
        reviews = get_dealer_reviews_from_cf(ep_review, dealer_id)
        context["reviews"] = reviews
        dealer = get_dealer_from_cf_by_id(ep_dealership, dealer_id)
        print(dealer,'==============')
        context["dealer"] = dealer
        return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context = {}
    dealer = get_dealer_from_cf_by_id(ep_dealership, dealer_id)
    context["dealer"] = dealer
    if request.method == 'GET':
        cars = CarModel.objects.all()
        context["cars"] = cars
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        if request.user.is_authenticated:
            username = request.user.username
            payload = dict()
            car_id = request.POST.get("car",'')
            if car_id != '':
                car = CarModel.objects.get(pk=car_id)
                payload["car_make"] = car.make.name
                payload["car_model"] = car.name

            payload["time"] = datetime.utcnow().isoformat()
            payload["name"] = username
            payload["dealership"] = dealer_id
            payload["review"] = request.POST.get("content","")
            payload["purchase"] = False

            if "purchasecheck" in request.POST:
                if request.POST["purchasecheck"] == 'on':
                    payload["purchase"] = True
            payload["purchase_date"] = request.POST["purchasedate"]

            new_payload = {}
            new_payload["review"] = payload
            post_request(ep_review, new_payload)
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
