from django.shortcuts import render
from django.http import JsonResponse
from .serializers import ItemSerializer

from . import models

# Create your views here.
def item_list(req):
    items = models.Item.objects.all()
    serializer = ItemSerializer(items, many=True)
    return JsonResponse(serializer.data, safe=False)
