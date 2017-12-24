from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader

from .models import Post
# Create your views here.


def index(request):
    post_list = Post.objects.order_by('date_time')
    context = {
        'post_list': post_list,
    }
    return render(request, 'blog/index.html', context)


def detail(request, blog_id):
    post = get_object_or_404(Post, pk=blog_id)
    context = {
        'post': post,
    }
    return render(request, 'blog/detail.html', context)
