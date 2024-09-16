from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView, CreateView, DetailView, ListView
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
    
class TripDetailView(DetailView):
    model = models.Trip

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trip = context['object']
        notes = trip.notes.all()
        context['notes'] = notes
        return context


class NoteCreateView(CreateView):
    model = models.Note
    fields = ["name", "description", "type", "rating", "trip"]
    success_url = reverse_lazy('note-list')

    def get_form(self):
        form = super(NoteCreateView, self).get_form()
        print(form.fields)
        form.fields['trip'].queryset = models.Trip.objects.filter(owner=self.request.user)
        return form

class NoteDetailView(DetailView):
    model = models.Note

class NoteListView(ListView):
    model = models.Note

    def get_queryset(self):
        return models.Note.objects.filter(trip__owner=self.request.user)
    