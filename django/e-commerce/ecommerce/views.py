from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
def index(req):
    return redirect('dashboard')

def dashboard(req):
    return render(req, 'ecommerce/dashboard.html')