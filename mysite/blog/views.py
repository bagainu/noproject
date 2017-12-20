from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader

from .models import Post
# Create your views here.


def index(request):
    post_list = Post.objects.order_by('date_time')
    context = {
        'post_list': post_list,
    }
    return render(request, 'blog/index.html', context)


def detail(request, title_slug):
    title = ' '.join([item for item in title_slug.strip().split('-')]).strip()
    try:
        post = Post.objects.get(blog_title=title)
    except Post.DoesNotExist:
        raise Http404('Blog "{0}" does not exist!'.format(title))
    context = {
        'post': post,
    }
    return render(request, 'blog/detail.html', context)
