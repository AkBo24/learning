from django.shortcuts import render, get_object_or_404

from .models import JobPosting

# Create your views here.
def index(req):
    active_posts = JobPosting.objects.filter(is_active=True)
    inactive_posts = JobPosting.objects.filter(is_active=False)

    context = {
        'active_posts': active_posts,
        'inactive_posts': inactive_posts
    }
    return render(req, 'job_board/index.html', context)

def job_posting(req, pk):
    post = get_object_or_404(JobPosting, pk=pk)

    context = {
        'post': post
    }

    return render(req, 'job_board/post.html', context)
