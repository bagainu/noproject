from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from book.models import Author, Press, Book

# Create your views here.

# Press view
class PressIndexView(View):

    def get(self, request):
        press_list = Press.objects.order_by('press_name')

        search_string = request.GET.get('search_string')
        if search_string:
            press_list = press_list.filter(
                Q(press_name__icontains=search_string)
            ).distinct()

        paginator = Paginator(press_list, 5)
        page = request.GET.get('page')
        try:
            page_press_list = paginator.page(page)
        except PageNotAnInteger:
            page_press_list = paginator.page(1)
        except EmptyPage:
            page_press_list = paginator.page(paginator.num_pages)
        except:
            page_press_list = None

        context = {
            'press_list': page_press_list,
        }
        return render(request, 'book/press_page/index.html', context)


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
