from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('<str:slug>', views.root_link, name='root-link'),
    path('link/create', views.create, name='create-link'),
]