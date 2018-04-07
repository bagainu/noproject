from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Prefetch
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from blog.models import Post
from book.forms import BookForm
from book.models import Author, Press, Book, BookTag
from comments.forms import CommentForm
from comments.models import Comment
from shelf.models import BookLog
from shelf.models import BookShelf

from utils.paginator import page_list

# Create your views here.

# Books view
class BookIndexView(View):

    def get(self, request):
        book_list = Book.objects.order_by('book_title')

        qs = request.GET.get('qs')
        if qs:
            book_list = book_list.filter(
                Q(book_title__icontains=qs) |
                Q(sub_title__icontains=qs) |
                Q(book_author__author_name__icontains=qs) |
                Q(book_press__press_name__icontains=qs) |
                Q(book_tag__name__icontains=qs)
            ).distinct()

        user_book_list = None
        if request.user.is_authenticated:
            user_shelf = get_object_or_404(BookShelf, shelf_owner=request.user)
            user_book_list = [ booklog.booklog_book for booklog in user_shelf.shelf_books.select_related('booklog_book') ]

        tag_list = BookTag.objects.all()

        context = {
            'book_list': page_list(request, book_list, 10), #book_list
            'tag_list': tag_list,
            'user_book_list': user_book_list,
        }
        return render(request, 'book/book_page/index.html', context)


@method_decorator(login_required, name='dispatch')
class BookCreateView(View):

    def get(self, request):
        book_form = BookForm()
        context = {
            'title': 'New Book',
            'book_form': book_form,
        }
        return render(request, 'book/book_page/create.html', context)

    def post(self, request):
        book_form = BookForm(request.POST or None, request.FILES or None)
        if book_form.is_valid():
            instance = book_form.save(commit=False)
            instance.save()
            book_form.save_m2m()
            return HttpResponseRedirect(instance.get_absolute_url())
        context = {
            'title': 'New Book',
            'book_form': book_form,
        }
        return render(request, 'book/book_page/create.html', context)


class BookDetailView(View):

    def get(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        user_booklog = None
        if request.user.is_authenticated:
            user_booklog = BookLog.objects.filter(booklog_owner=request.user, booklog_book=book).first()

        # the booklog_comment is the related_query_name of BookLog and used as a reverse lookup from Comment
        book_comments = Comment.objects.filter(booklog_comment__booklog_book=book, parent_comment=None).order_by('-comment_date_time')
        page_book_comments = page_list(request, book_comments, 5, 'c-page') 

        book_posts = Post.objects.filter(booklog_post__booklog_book=book).order_by('-create_date_time')
        page_book_posts = page_list(request, book_posts, 5, 'p-page')

        context = {
            'booklog': user_booklog,
            'book': book,
            'book_comments': page_book_comments,
            'book_posts': page_book_posts,
            'comment_form': CommentForm(),
        }
        return render(request, 'book/book_page/detail.html', context)

    @login_required
    def post(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        if request.user.is_authenticated:
            comment_form = CommentForm(request.POST, request.FILES)
            if comment_form.is_valid():
                comment_instance = comment_form.save(commit=False)
                parent_id = request.POST.get('parent_id')
                if parent_id is not None:
                    parent_obj = Comment.objects.get(pk=int(parent_id))
                else:
                    return self.get(request, book_id)
                comment_instance.parent_comment = parent_obj
                comment_instance.comment_user = request.user
                comment_instance.content_type = ContentType.objects.get_for_model(BookLog)
                comment_instance.content_object = BookLog.objects.get(booklog_book=book, booklog_owner=parent_obj.comment_user) 
                comment_instance.object_id = book.id
                comment_form.save()
                comment_form.save_m2m()
                return HttpResponseRedirect(book.get_absolute_url())
        return self.get(request, book_id)


@method_decorator(login_required, name='dispatch')
class BookUpdateView(View):

    def get(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        book_form = BookForm(instance=book)
        context = {
            'title': 'Edit Book',
            'book_form': book_form,
        }
        return render(request, 'book/book_page/create.html', context)

    def post(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        book_form = BookForm(request.POST or None, request.FILES or None, instance=book)
        if book_form.is_valid():
            instance = book_form.save(commit=False)
            instance.save()
            book_form.save_m2m()
            return HttpResponseRedirect(instance.get_absolute_url())
        return self.get(request, book_id)


@method_decorator(login_required, name='dispatch')
class BookDeleteView(View):

    def get(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        context = {
            'book': book,
        }
        return render(request, 'book/book_page/delete.html', context)

    def post(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        book.delete()
        return HttpResponseRedirect(reverse("book:book_index"))
