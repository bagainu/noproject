from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.forms import modelformset_factory, inlineformset_factory, forms
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse
from django.utils.html import format_html

from .models import Post, PostTag
from .forms import PostForm
from taggit.models import Tag
from comments.forms import CommentForm
from comments.models import Comment
from shelf.models import BookLog

from utils.paginator import page_list
# Create your views here.


def index(request):
    post_list = Post.objects.order_by('-update_date_time') # use '-' to order items in reversed order

    owner_id = request.GET.get('owner_id')
    if owner_id:
        user = get_object_or_404(get_user_model(), pk=owner_id)
        post_list = post_list.filter(blog_author=user)

    qs = request.GET.get('qs')
    if qs:
        post_list = post_list.filter(
            Q(blog_title__icontains=qs) |
            Q(blog_content__icontains=qs) |
            Q(blog_author__username__icontains=qs) |
            Q(blog_author__email__icontains=qs) |
            Q(blog_tag__name__icontains=qs)
        ).distinct()

    page_post_list = page_list(request, post_list, 5)
    tag_list = PostTag.objects.all()

    context = {
        'title': 'Posts',
        'post_list': page_post_list, #post_list
        'tag_list': tag_list,
    }
    return render(request, 'blog/index.html', context)


@login_required
def index_own(request, user_id):
    user = get_object_or_404(get_user_model(), pk=user_id)
    post_list = Post.objects.filter(blog_author=user).order_by('-update_date_time') # use '-' to order items in reversed order

    qs = request.GET.get('qs')
    if qs:
        post_list = post_list.filter(
            Q(blog_title__icontains=qs) |
            Q(blog_content__icontains=qs) |
            Q(blog_author__username__icontains=qs) |
            Q(blog_author__email__icontains=qs) |
            Q(blog_tag__name__icontains=qs)
        ).distinct()

    page_post_list = page_list(request, post_list, 5)
    tag_list = PostTag.objects.all()

    title = format_html("""<i>{0}</i>'s Post""".format(user.username))
    if request.user == user:
        title = 'My Posts'

    context = {
        'title': title,
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

    post_comments = post.blog_comment.filter(parent_comment=None).order_by('-comment_date_time')
    page_post_comments = page_list(request, post_comments, 10)
    context = {
        'booklog': post.content_object,
        'post': post,
        'post_comments': page_post_comments,
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
        return HttpResponseRedirect(reverse("blog:blog_index_own", kwargs={ 'user_id': request.user.id }))
    context = {
        'post': post,
    }
    return render(request, 'blog/delete.html', context)


@login_required
def ajax_vote_up(request, blog_id):
    if not request.is_ajax():
        raise Http404('Not an ajax call')
    post = get_object_or_404(Post, pk=blog_id)
    if request.method == 'POST' and not post.votes.exists(request.user.id):
        post.votes.up(request.user.id)
        return JsonResponse({'count': post.votes.count(0) })
    return JsonResponse({'count': -1 })


