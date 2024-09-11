from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('job/<int:pk>/', views.job_posting),
]