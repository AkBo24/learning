from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('dashboard/', views.trips_list, name='trips-list'),
    path('dashboard/trip/create/', views.TripCreateView.as_view(), name='trip-create'),
    path('dashboard/trip/<int:pk>/', views.trips_list, name='trip-detail'),
    path('', views.trips_list, name='note-list'),
    path('', views.trips_list, name='note-create'),
]
