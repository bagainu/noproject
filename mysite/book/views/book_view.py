from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from book.forms import BookForm
from book.models import Author, Press, Book, BookTag
from comments.forms import CommentForm
from comments.models import Comment
from shelf.models import BookLog

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

        paginator = Paginator(book_list, 5)
        page = request.GET.get('page')
        try:
            page_book_list = paginator.page(page)
        except PageNotAnInteger:
            page_book_list = paginator.page(1)
        except EmptyPage:
            page_book_list = paginator.page(paginator.num_pages)
        except:
            page_book_list = None

        tag_list = BookTag.objects.all()

        context = {
            'book_list': page_book_list, #post_list
            'tag_list': tag_list,
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
        booklog = None
        if request.user.is_authenticated:
            booklog = BookLog.objects.filter(booklog_owner=request.user, booklog_book=book).first()
        context = {
            'booklog': booklog,
            'book': book,
            # 'book_comments': book.book_comment.filter(parent_comment=None).order_by('-comment_date_time'),
            'book_comments': [],
            'comment_form': CommentForm(),
        }
        return render(request, 'book/book_page/detail.html', context)

    def post(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        if request.user.is_authenticated:
            comment_form = CommentForm(request.POST, request.FILES)
            if comment_form.is_valid():
                comment_instance = comment_form.save(commit=False)
                comment_instance.comment_user = request.user
                comment_instance.content_type = ContentType.objects.get_for_model(Book)
                comment_instance.content_object = book 
                comment_instance.object_id = book.id
                parent_id = request.POST.get('parent_id')
                if parent_id is not None:
                    comment_instance.parent_comment = Comment.objects.get(pk=int(parent_id))
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
