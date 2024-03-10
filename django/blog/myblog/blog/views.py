from django.shortcuts import render
from .models import Post

# Create your views here.
def post_list(request):
    posts = Post.objects.all()
    posts = [
        {'title': 'My first blog', 'body': 'Bite my shiny metal ass!'}
    ]
    return render(request, 'post_list.html', {'posts': posts})