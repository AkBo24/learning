from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('url-params/<str:dish>', views.url_params)
]