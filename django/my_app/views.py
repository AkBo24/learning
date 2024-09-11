from django.shortcuts import render, HttpResponse

# Create your views here.
def index(req):
    return HttpResponse("Hello World")

def about(req):
    return HttpResponse("<h1>About</h1>")

def hello(req, name):
    return HttpResponse(f"Hello {name}")