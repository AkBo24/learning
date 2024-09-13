from django.urls import path

from . import views

urlpatterns = [
    path('', views.LinkListView.as_view(), name='link-list'),
    path('', views.LinkListView.as_view(), name='link-create'),
    path('', views.LinkListView.as_view(), name='link-update'),
    path('', views.LinkListView.as_view(), name='link-delete'),
]
