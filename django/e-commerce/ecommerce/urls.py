from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('dashboard', views.WebsiteListView.as_view(), name='dashboard'),
    path('dashboard/create', views.WebsiteCreateView.as_view(), name='website-create')
]
