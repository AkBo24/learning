from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy

from . import models

# Create your views here.
def index(req):
    return redirect('dashboard')


class WebsiteListView(ListView):
    model = models.Website
    # template_name = "ecommerce/dashboard.html"

    # def get_queryset(self):
    #     # print('hi', models.Website.objects.filter(name="t/"))
    #     return models.Website.objects.all()

    # def get_queryset(self):
    #     return models.Note.objects.filter(trip__owner=self.request.user)

class WebsiteCreateView(CreateView):
    model = models.Website
    fields = "__all__"
    # template_name = 'ecommerce/website_create.html'
    success_url = reverse_lazy('dashboard')