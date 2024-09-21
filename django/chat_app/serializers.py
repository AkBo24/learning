from rest_framework import serializers

from . import models

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChatRoom
        fields = "__all__"

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Message
        fields = "__all__"