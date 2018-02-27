from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from book.models import Author, Press, Book

# Create your views here.

# Author view
class AuthorIndexView(View):

    def get(self, request):
        author_list = Author.objects.order_by('author_name')

        search_string = request.GET.get('search_string')
        if search_string:
            author_list = author_list.filter(
                Q(author_name__icontains=search_string) |
                Q(author_intro__icontains=search_string)
            ).distinct()

        paginator = Paginator(author_list, 5)
        page = request.GET.get('page')
        try:
            page_author_list = paginator.page(page)
        except PageNotAnInteger:
            page_author_list = paginator.page(1)
        except EmptyPage:
            page_author_list = paginator.page(paginator.num_pages)
        except:
            page_author_list = None

        context = {
            'author_list': page_author_list,
        }
        return render(request, 'book/author_page/index.html', context)


class AuthorCreateView(View):

    def get(self, request):
        return HttpResponse('Create get')

    def post(self, request):
        return HttpResponse('Create post')


class AuthorDetailView(View):

    def get(self, request, author_id):
        return HttpResponse('Detail')


class AuthorUpdateView(View):

    def get(self, request, author_id):
        return HttpResponse('Update get')

    def post(self, request, author_id):
        return HttpResponse('Update post')


class AuthorDeleteView(View):

    def get(self, request, author_id):
        return HttpResponse('Author Delete get')

    def post(self, request, author_id):
        return HttpResponse('Author Delete post')

