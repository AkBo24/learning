from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.http import JsonResponse

from django.urls import reverse_lazy

from . import models
from . import serializers

from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView

# Create your views here.
def index(req):
    return redirect('dashboard')


class WebsiteListView(ListView):
    model = models.Website
    # template_name = "ecommerce/dashboard.html"

    def get_queryset(self):
        print('hi', models.Website.objects.all())
        return models.Website.objects.all()

    def get_queryset(self):
        return models.Website.objects.filter(owner=self.request.user)

class WebsiteCreateView(CreateView):
    model = models.Website
    fields = ["name", "description", "url"]
    # template_name = 'ecommerce/website_create.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
class WebisteUpdateView(UpdateView):
    model = models.Website
    fields = ["name", "description", "url"]
    success_url = reverse_lazy('dashboard')
    
    
class WebsiteDetailView(DetailView):
    model = models.Website
    

class WebsiteDeleteView(DeleteView):
    model = models.Website
    success_url = reverse_lazy('dashboard')

class APIWebsiteList(ListAPIView):
    queryset = models.Website.objects.all()
    serializer_class = serializers.WebsiteSerializer

class APIWebsiteDetail(RetrieveUpdateDestroyAPIView):
    queryset = models.Website.objects.all()
    serializer_class = serializers.WebsiteSerializer
