from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.ChatRoomListView.as_view()),
    path('room/<int:pk>', views.ChatRoomDetailView.as_view(), name="room"),
    path('api/chat-rooms', views.APIChatRoomList.as_view()),         # GET all chat-rooms
    path('api/chat-rooms/<int:pk>', views.APIChatRoom.as_view()), # GET,POST,UPDATE,DELETE chat-room
    path('api/chat-rooms/<int:pk>/messages', views.APIChatRoomMessageList.as_view()),          # GET,POST,UPDATE,DELETE messages
    path('api/messages', views.APIMessageList.as_view()),          # GET all messages
]