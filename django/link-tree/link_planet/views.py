from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from . import models

# Create your views here.
class LinkListView(ListView):
    model = models.Link

class LinkCreateView(CreateView):
    model = models.Link
    fields = "__all__" # use all field variables in the model
    success_url = reverse_lazy('link-list')

class LinkUpdateView(UpdateView):
    model = models.Link
    fields = ["text", "url"]
    success_url = reverse_lazy('link-list')

class LinkDeleteView(DeleteView):
    model = models.Link
    success_url = reverse_lazy('link-list')
