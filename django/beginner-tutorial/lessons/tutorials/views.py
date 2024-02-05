from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    content = "<h1>Navigate to /<lesson> to see individual lessons </h1>"
    return HttpResponse(content)