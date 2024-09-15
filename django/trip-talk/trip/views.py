from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm

from . import models

# Create your views here.
class HomeView(TemplateView):
    template_name = "trip/index.html"

def trips_list(req):
    trips = models.Trip.objects.filter(owner=req.user)
    context = {
        'trips': trips
    }
    return render(req, 'trip/trips_list.html', context)

class SignupView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"
