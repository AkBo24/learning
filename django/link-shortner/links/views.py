from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import Link
from .forms import LinkForm

# Create your views here.
def index(req):

    context = {
        'links': Link.objects.all()
    }

    return render(req, 'links/index.html', context)


def root_link(req, slug):
    link = get_object_or_404(Link, slug=slug)
    link.click()

    return redirect(link.url)

def create(request):
    if request.method == "POST":
        form = LinkForm(request.POST)
        if form.is_valid():
            # if the form is valid - then process
            form.save()
            return redirect(reverse('home'))
    
    else:
        form = LinkForm()

    context = {
        "form": form
    }
    return render(request, 'links/create.html', context)