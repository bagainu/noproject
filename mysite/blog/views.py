from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from .models import Post, Author
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


def login(request, author_id):
    if request.method == 'POST':
        try:
            author = Author.objects.get(pk=author_id)
        except:
            new_author = Author(email=request.POST['user_email'], user_pwd=request.POST['user_password'])
            new_author.save()
            return HttpResponseRedirect(reverse('blog:blog_login', args=(new_author.id, )))
        else:
            if author.user_pwd == request.POST['user_password']:
                return render(request, 'blog/login.html', {'title_text': 'Signed in'})
            else:
                return render(request, 'blog/login.html', {'title_text': 'Password error'})
    else:
        author = Author.objects.get()
        return render(request, 'blog/login.html', {'title_text': 'Sign in'})


def response_page(request):
    return render(request, 'blog/response_page.html', { 'messages': 'Logged in' })


