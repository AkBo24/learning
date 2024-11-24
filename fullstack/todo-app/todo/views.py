from rest_framework import viewsets

from . import models
from . import serializers

class TodoViewSet(viewsets.ModelViewSet):
    queryset = models.Todo.objects.all()
    serializer_class = serializers.TodoSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)