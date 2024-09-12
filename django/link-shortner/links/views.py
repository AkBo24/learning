from django.shortcuts import render, get_object_or_404, redirect, HttpResponse

from .models import Link

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