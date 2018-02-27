from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from book.models import Author, Press, Book

# Create your views here.

# Books view
class BookIndexView(View):

    def get(self, request):
        book_list = Book.objects.order_by('book_title')

        search_string = request.GET.get('search_string')
        if search_string:
            book_list = book_list.filter(
                Q(book_title__icontains=search_string) |
                Q(sub_title__icontains=search_string) |
                Q(book_author__author_name__icontains=search_string) |
                Q(book_press__press_name__icontains=search_string)
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

        context = {
            'book_list': page_book_list, #post_list
        }
        return render(request, 'book/book_page/index.html', context)


class BookCreateView(View):

    def get(self, request):
        return HttpResponse('Create get')

    def post(self, request):
        return HttpResponse('Create post')


class BookDetailView(View):

    def get(self, request, book_id):
        return HttpResponse('Detail')


class BookUpdateView(View):

    def get(self, request, book_id):
        return HttpResponse('Update get')

    def post(self, request, book_id):
        return HttpResponse('Update post')


class BookDeleteView(View):

    def get(self, request, book_id):
        return HttpResponse('Book Delete get')

    def post(self, request, book_id):
        return HttpResponse('Book Delete post')
