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

class TripCreateView(CreateView):
    model = models.Trip
    fields = ["city", "country", "start_date", "end_date"]
    success_url = reverse_lazy('trips-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

