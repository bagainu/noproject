from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.forms import modelformset_factory, inlineformset_factory, forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post, Author
from .forms import PostForm
from comments.forms import CommentForm
# Create your views here.


def index(request):
    post_list = Post.objects.order_by('-update_date_time') # use '-' to order items in reversed order
    print(request.GET)

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
    if not request.user.is_authenticated:
        context = {
            'post': post,
            'post_comments': post.blog_comment.order_by('-comment_date_time'),
        }
        return render(request, 'blog/detail.html', context)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment_instance = comment_form.save(commit=False)
            comment_instance.comment_user = request.user
            comment_instance.content_type = ContentType.objects.get_for_model(Post)
            comment_instance.content_object = post
            comment_instance.object_id = post.id
            comment_instance.save()
            comment_form.save_m2m()
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        context = {
            'post': post,
            'post_comments': post.blog_comment.order_by('-comment_date_time'),
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
    # DeleteNewFormSet = forms(Post, fields=[])
    # if request.method == 'POST':
    #     print(request.POST)
    #     post_form = DeleteNewFormSet(request.POST, instance=post)
    #     if post_form.is_valid():
    #         print(post)
    #         post.delete()
    post.delete()
    return HttpResponseRedirect(reverse('blog:blog_index'))




# def login(request, author_id):
#     if request.method == 'POST':
#         try:
#             author = Author.objects.get(pk=author_id)
#         except:
#             new_author = Author(email=request.POST['user_email'], user_pwd=request.POST['user_password'])
#             new_author.save()
#             return HttpResponseRedirect(reverse('blog:blog_login', args=(new_author.id, )))
#         else:
#             if author.user_pwd == request.POST['user_password']:
#                 return render(request, 'blog/login.html', {'title_text': 'Signed in'})
#             else:
#                 return render(request, 'blog/login.html', {'title_text': 'Password error'})
#     else:
#         author = Author.objects.get()
#         return render(request, 'blog/login.html', {'title_text': 'Sign in'})


# def response_page(request):
#     return render(request, 'blog/response_page.html', { 'messages': 'Logged in' })


