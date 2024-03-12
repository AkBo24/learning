from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import PostViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('', include(router.urls))
    # path('', views.post_list, name='post_list'),
    # path('post/new', views.post_create, name='post_create'),
    # path('post/<int:pk>/edit', views.post_edit, name='post_edit')
]