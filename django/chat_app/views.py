from django.shortcuts import render, HttpResponse

from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.exceptions import NotFound

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
    serializer_class = MessageSerializer

    def get_queryset(self):
        pk = self.kwargs.get("pk")

        try:
            chat_room = ChatRoom.objects.get(pk=pk)
        except ChatRoom.DoesNotExist:
            raise NotFound(f"Chat room with id {pk} does not exist.")
        
        return Message.objects.filter(chatRoom=chat_room)

    def perform_create(self, serializer):
        pk = self.kwargs.get("pk")

        try:
            chat_room = ChatRoom.objects.get(pk=pk)
        except ChatRoom.DoesNotExist:
            raise NotFound(f"Chat room with id {pk} does not exist.")
        
        serializer.save(chatRoom=chat_room)


class APIMessageList(ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer