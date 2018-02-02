from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.forms import modelformset_factory, inlineformset_factory, forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post
from .forms import PostForm
from comments.forms import CommentForm
from comments.models import Comment
# Create your views here.


def index(request):
    post_list = Post.objects.order_by('-update_date_time') # use '-' to order items in reversed order

    search_string = request.GET.get('search_string')
    if search_string:
        post_list = post_list.filter(
            Q(blog_title__icontains=search_string) |
            Q(blog_content__icontains=search_string) |
            Q(blog_author__username__icontains=search_string) |
            Q(blog_author__email__icontains=search_string)
        ).distinct()

    paginator = Paginator(post_list, 5)
    page = request.GET.get('page')
    try:
        page_post_list = paginator.page(page)
    except PageNotAnInteger:
        page_post_list = paginator.page(1)
    except EmptyPage:
        page_post_list = paginator.page(paginator.num_pages)
    except:
        page_post_list = None

    title_msg = 'Not Authenticated'
    if request.user.is_authenticated:
        title_msg = 'Authenticated'

    context = {
        'post_list': page_post_list, #post_list
    }
    return render(request, 'blog/index.html', context)


# Create
def create(request):
    if request.method == 'POST':
        # print(request.POST)
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            instance = post_form.save(commit=False) 
            instance.blog_author = request.user
            instance.save()
            return HttpResponseRedirect(instance.get_absolute_url())
    else:
        post_form = PostForm()
        context = {
            'post_form': post_form,
        }
        return render(request, 'blog/create.html', context)


# Read
def detail(request, blog_id):
    post = get_object_or_404(Post, pk=blog_id)
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment_instance = comment_form.save(commit=False)
            comment_instance.comment_user = request.user
            comment_instance.content_type = ContentType.objects.get_for_model(Post)
            comment_instance.content_object = post
            comment_instance.object_id = post.id
            parent_id = request.POST.get('parent_id')
            if parent_id is not None:
                comment_instance.parent_comment = Comment.objects.get(pk=int(parent_id))
            comment_form.save()
            comment_form.save_m2m()
            return HttpResponseRedirect(post.get_absolute_url())
    context = {
        'post': post,
        'post_comments': post.blog_comment.filter(parent_comment=None).order_by('-comment_date_time'),
        'comment_form': CommentForm(),
    }
    return render(request, 'blog/detail.html', context)


# Update
def update(request, blog_id):
    post = get_object_or_404(Post, pk=blog_id)
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES, instance=post)
        if post_form.is_valid():
            instance = post_form.save(commit=False) 
            instance.save()
            return HttpResponseRedirect(instance.get_absolute_url())
    else:
        post_form = PostForm(instance=post)
        context = {
            'post_form': post_form,
        }
        return render(request, 'blog/create.html', context)


# Delete
def delete(request, blog_id):
    post = get_object_or_404(Post, pk=blog_id)
    if request.method == "POST":
        post.delete()
        return HttpResponseRedirect(reverse("blog:blog_index"))
    context = {
        'post': post,
    }
    return render(request, 'blog/delete.html', context)



