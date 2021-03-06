from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from book.forms import AuthorForm 
from book.models import Author, Press, Book

from utils.paginator import page_list

# Create your views here.

# Author view
class AuthorIndexView(View):

    def get(self, request):
        author_list = Author.objects.order_by('author_name')

        qs = request.GET.get('qs')
        if qs:
            author_list = author_list.filter(
                Q(author_name__icontains=qs) |
                Q(author_intro__icontains=qs)
            ).distinct()

        page_author_list = page_list(request, author_list, 5)
        context = {
            'author_list': page_author_list,
        }
        return render(request, 'book/author_page/index.html', context)


@method_decorator(login_required, name='dispatch')
class AuthorCreateView(View):

    def get(self, request):
        author_form = AuthorForm()
        context = {
            'title': 'New Author',
            'author_form': author_form,
        }
        return render(request, 'book/author_page/create.html', context)

    def post(self, request):
        author_form = AuthorForm(request.POST or None, request.FILES or None)
        if author_form.is_valid():
            instance = author_form.save(commit=False)
            instance.save()
            author_form.save_m2m()
            return HttpResponseRedirect(instance.get_absolute_url())
        context = {
            'title': 'New Author',
            'book_form': author_form,
        }
        return render(request, 'book/author_page/create.html', context)


class AuthorDetailView(View):

    def get(self, request, author_id):
        author = get_object_or_404(Author, pk=author_id)
        context = {
            'author': author,
            # books of this author
        }
        return render(request, 'book/author_page/detail.html', context)


@method_decorator(login_required, name='dispatch')
class AuthorUpdateView(View):

    def get(self, request, author_id):
        author = get_object_or_404(Author, pk=author_id)
        author_form = AuthorForm(instance=author)
        context = {
            'title': 'Edit Author',
            'author_form': author_form,
        }
        return render(request, 'book/author_page/create.html', context)

    def post(self, request, author_id):
        author = get_object_or_404(Author, pk=author_id)
        author_form = AuthorForm(request.POST or None, request.FILES or None, instance=author)
        if author_form.is_valid():
            instance = author_form.save(commit=False)
            instance.save()
            author_form.save_m2m()
            return HttpResponseRedirect(instance.get_absolute_url())
        context = {
            'title': 'Edit Author',
            'author_form': author_form,
        }
        return render(request, 'book/author_page/create.html', context)


@method_decorator(login_required, name='dispatch')
class AuthorDeleteView(View):

    def get(self, request, author_id):
        author = get_object_or_404(Author, pk=author_id)
        context = {
            'author': author,
        }
        return render(request, 'book/author_page/delete.html', context)

    def post(self, request, author_id):
        author = get_object_or_404(Author, pk=author_id)
        author.delete()
        return HttpResponseRedirect(reverse("book:author_index"))

