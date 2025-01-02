from django.urls import path

from . import views

urlpatterns = [
    path('', views.LinkListView.as_view(), name='link-list'),
    path('link/create/', views.LinkCreateView.as_view(), name='link-create'),
    path('link/<int:pk>/update', views.LinkUpdateView.as_view(), name='link-update'),
    path('link/<int:pk>/delete/', views.LinkDeleteView.as_view(), name="link-delete"),
]
