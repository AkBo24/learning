from django.shortcuts import render, HttpResponse

# Create your views here.
def index(req):
    context = {
        'movies': ['Paprika', 'Beau is Afraid', 'Tenent']
    }
    return render(req, 'movies/index.html',context)

def about(req):
    return render(req, 'movies/about.html')