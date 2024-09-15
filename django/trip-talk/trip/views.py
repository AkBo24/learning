from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView, ListView

from . import models

# Create your views here.
class HomeView(TemplateView):
    template_name = "trip/index.html"

def trips_list(req):
    trips = models.Trip.objects.all()
    context = {
        'trips': trips
    }
    return render(req, 'trip/trips_list.html', context)
