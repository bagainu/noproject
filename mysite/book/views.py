from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View

# Create your views here.

# Books view
class BookIndexView(View):

    def get(self, request):
        return HttpResponse('Index')


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


# Author view
class AuthorIndexView(View):

    def get(self, request):
        return HttpResponse('Index')


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


# Press view
class PressIndexView(View):

    def get(self, request):
        return HttpResponse('Index')


class PressCreateView(View):

    def get(self, request):
        return HttpResponse('Create get')

    def post(self, request):
        return HttpResponse('Create post')


class PressDetailView(View):

    def get(self, request, press_id):
        return HttpResponse('Detail')


class PressUpdateView(View):

    def get(self, request, press_id):
        return HttpResponse('Update get')

    def post(self, request, press_id):
        return HttpResponse('Update post')


class PressDeleteView(View):

    def get(self, request, press_id):
        return HttpResponse('Delete get')

    def post(self, request, press_id):
        return HttpResponse('Delete post')

