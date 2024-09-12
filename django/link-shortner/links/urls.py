from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('<str:slug>', views.root_link, name='root-link'),
    path('create', views.index, name='create-link'),
]