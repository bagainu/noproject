from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.forms import modelformset_factory, inlineformset_factory, forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post, PostTag
from .forms import PostForm
from taggit.models import Tag
from comments.forms import CommentForm
from comments.models import Comment
from shelf.models import BookLog
# Create your views here.


def index(request):
    post_list = Post.objects.order_by('-update_date_time') # use '-' to order items in reversed order

    qs = request.GET.get('qs')
    if qs:
        post_list = post_list.filter(
            Q(blog_title__icontains=qs) |
            Q(blog_content__icontains=qs) |
            Q(blog_author__username__icontains=qs) |
            Q(blog_author__email__icontains=qs) |
            Q(blog_tag__name__icontains=qs)
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

    tag_list = PostTag.objects.all()

    context = {
        'post_list': page_post_list, #post_list
        'tag_list': tag_list,
    }
    return render(request, 'blog/index.html', context)


# Create
@login_required
def create(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            instance = post_form.save(commit=False) 
            instance.blog_author = request.user
            instance.save()
            post_form.save_m2m()
            return HttpResponseRedirect(instance.get_absolute_url())
    else:
        post_form = PostForm()
        context = {
            'title': 'New Blog',
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
        'booklog': post.content_object,
        'post': post,
        'post_comments': post.blog_comment.filter(parent_comment=None).order_by('-comment_date_time'),
        'comment_form': CommentForm(),
    }
    return render(request, 'blog/detail.html', context)


# Update
@login_required
def update(request, blog_id):
    post = get_object_or_404(Post, pk=blog_id)
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES, instance=post)
        if post_form.is_valid():
            instance = post_form.save(commit=False) 
            instance.save()
            post_form.save_m2m()
            return HttpResponseRedirect(instance.get_absolute_url())
    else:
        post_form = PostForm(instance=post)
        context = {
            'title': 'Edit Blog',
            'post_form': post_form,
        }
        return render(request, 'blog/create.html', context)


# Delete
@login_required
def delete(request, blog_id):
    post = get_object_or_404(Post, pk=blog_id)
    if request.method == "POST":
        post.delete()
        return HttpResponseRedirect(reverse("blog:blog_index"))
    context = {
        'post': post,
    }
    return render(request, 'blog/delete.html', context)



