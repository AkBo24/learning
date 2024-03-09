from django.shortcuts import render
from django.http import HttpResponse

def say_hello(request):
    # return  HttpResponse("Hello, django!")
    return render(request, 'hello.html', context={'name': 'MELON LORD'})
