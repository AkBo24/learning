from rest_framework import serializers

from . import models

class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Website
        fields = "__all__"