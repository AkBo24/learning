from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class ChatRoom(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_rooms")

    def __str__(self):
        return f"{self.name} | {self.owner.username}"

class Message(models.Model):
    content = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cessages")
    chatRoom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.content[:5]} | {self.owner} | {self.chatRoom.name}"