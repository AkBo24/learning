from rest_framework import serializers

from . import models

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Todo
        fields = ["id", "title", "description", "completed"]
        read_only_fields = ['id', 'created_at', 'updated_at', 'owner']