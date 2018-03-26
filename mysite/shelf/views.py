from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from .models import BookLog, BookShelf
from .forms import BookLogForm
from comments.forms import CommentForm
from comments.models import Comment
from blog.forms import PostForm

# Create your views here.


class BookShelfView(View):
    """
    BookShelf view = BookLog index view
    """
    is_public = True

    def get(self, request):
        book_shelf = get_list_or_404(BookShelf, shelf_public=self.is_public)[0]
        booklogs_list = book_shelf.shelf_books.all()

        qs = request.GET.get('qs')
        if qs:
            booklogs_list = booklogs_list.filter(
                Q(booklog_book__book_title__icontains=qs) |
                Q(booklog_book__sub_title__icontains=qs) |
                Q(booklog_book__book_author__author_name__icontains=qs) |
                Q(booklog_book__book_press__press_name__icontains=qs) |
                Q(booklog_book__book_tag__name__icontains=qs) |
                Q(booklog_intro__icontains=qs)
            ).distinct()

        paginator = Paginator(booklogs_list, 20)
        page = request.GET.get('page')
        try:
            page_booklogs_list = paginator.page(page)
        except PageNotAnInteger:
            page_booklogs_list = paginator.page(1)
        except EmptyPage:
            page_booklogs_list = paginator.page(paginator.num_pages)
        except:
            page_booklogs_list = None

        context = {
            'title': book_shelf.shelf_name,
            'booklog_list': page_booklogs_list,
        }
        return render(request, 'shelf/shelf.html', context)
    

@method_decorator(login_required, name='dispatch')
class BookLogCreateView(View):

    def get(self, request):
        return HttpResponse('create get')
    
    def post(self, request):
        return HttpResponse('create post')


@method_decorator(login_required, name='dispatch')
class BookLogPostCreateView(View):

    def get(self, request, booklog_id):
        booklog = get_object_or_404(BookLog, pk=booklog_id)
        post_form = PostForm()
        context = {
            'booklog': booklog,
            'title': 'New Post',
            'post_form': post_form,
        }
        return render(request, 'blog/create.html', context)
    
    def post(self, request, booklog_id):
        booklog = get_object_or_404(BookLog, pk=booklog_id)
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            instance = post_form.save(commit=False) 
            instance.blog_author = request.user
            instance.content_type = ContentType.objects.get_for_model(BookLog)
            instance.content_object = booklog
            instance.object_id = booklog.id
            instance.save()
            post_form.save_m2m()
            return HttpResponseRedirect(instance.get_absolute_url())
        self.get(request, booklog_id)


class BookLogDetailView(View):

    def get(self, request, booklog_id):
        booklog = get_object_or_404(BookLog, pk=booklog_id)
        booklog_posts = booklog.booklog_post.all().order_by('-update_date_time')
        paginator = Paginator(booklog_posts, 20)
        page = request.GET.get('page')
        try:
            page_booklog_posts_list = paginator.page(page)
        except PageNotAnInteger:
            page_booklog_posts_list = paginator.page(1)
        except EmptyPage:
            page_booklog_posts_list = paginator.page(paginator.num_pages)
        except:
            page_booklog_posts_list = None

        context = {
            'booklog': booklog,
            'booklog_comments': booklog.booklog_comment.filter(parent_comment=None).order_by('-comment_date_time'),
            'booklog_posts': page_booklog_posts_list,
            'comment_form': CommentForm(),
        }
        return render(request, 'shelf/detail.html', context)
    
    def post(self, request, booklog_id):
        booklog = get_object_or_404(BookLog, pk=booklog_id)
        comment_form = CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment_instance = comment_form.save(commit=False)
            comment_instance.comment_user = request.user
            comment_instance.content_type = ContentType.objects.get_for_model(BookLog)
            comment_instance.content_object = booklog
            comment_instance.object_id = booklog.id
            comment_form.save()
            comment_form.save_m2m()
            return HttpResponseRedirect(booklog.get_absolute_url())
        return self.get(request, booklog_id)


@method_decorator(login_required, name='dispatch')
class BookLogUpdateView(View):

    def get(self, request, booklog_id):
        return HttpResponse('update get')
    
    def post(self, request, booklog_id):
        return HttpResponse('update post')


@method_decorator(login_required, name='dispatch')
class BookLogDeleteView(View):

    def get(self, request, booklog_id):
        return HttpResponse('delete get')
    
    def post(self, request, booklog_id):
        return HttpResponse('delete post')

