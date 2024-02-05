from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    content = "<h1>Navigate to /<lesson> to see individual lessons </h1>"
    return HttpResponse(content)

def url_params(request, dish):
    items = {
        'pizza': 'From Toni\'s!',
        'cappuccino': 'From Cafe Greco!'
    }

    description = items[dish]
    return HttpResponse(f"<h2>{dish}</h2><p>{description}</p>")