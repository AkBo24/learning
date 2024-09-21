from django.contrib import admin
from django.urls import path, include

from .views import index, room

urlpatterns = [
    path('', index),
    path('room', room)
]