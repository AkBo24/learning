from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('dashboard', views.WebsiteListView.as_view(), name='dashboard'),
    path('dashboard/create', views.WebsiteCreateView.as_view(), name='website-create'),
    path('dashboard/<int:pk>', views.WebsiteDetailView.as_view(), name='website-detail'),
    path('dashboard/<int:pk>/update', views.WebisteUpdateView.as_view(), name='website-update'),
    path('dashboard/<int:pk>/delete', views.WebsiteDetailView.as_view(), name='website-delete'),
]
