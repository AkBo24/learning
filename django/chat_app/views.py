from django.shortcuts import render, HttpResponse

from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView

from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer

# Create your views here.
def index(req):
    return HttpResponse('test')

def room(req):
    return HttpResponse('room')

class APIChatRoomList(ListAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer

class APIChatRoom(RetrieveUpdateDestroyAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer

class APIChatRoomMessageList(ListCreateAPIView):
    print(Message.objects.filter(chatRoom=1))
    queryset = Message.objects.filter(chatRoom_id=1)
    serializer_class = MessageSerializer

# class APIChatRoomMessageCreate(CreateAPIView):


class APIMessageList(ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer