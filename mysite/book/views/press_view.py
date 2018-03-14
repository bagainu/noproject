from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from book.models import Author, Press, Book
from book.forms import PressForm

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


@method_decorator(login_required, name='dispatch')
class PressCreateView(View):

    def get(self, request):
        press_form = PressForm()
        context = {
            'title': 'New Press',
            'press_form': press_form,
        }
        return render(request, 'book/press_page/create.html', context)

    def post(self, request):
        press_form = PressForm(request.POST or None, request.FILES or None)
        if press_form.is_valid():
            instance = press_form.save(commit=False)
            instance.save()
            press_form.save_m2m()
            return HttpResponseRedirect(instance.get_absolute_url())
        context = {
            'title': 'New Press',
            'press_form': press_form,
        }
        return render(request, 'book/press_page/create.html', context)


class PressDetailView(View):

    def get(self, request, press_id):
        press = get_object_or_404(Press, pk=press_id)
        context = {
            'press': press,
            # books of this press 
        }
        return render(request, 'book/press_page/detail.html', context)


@method_decorator(login_required, name='dispatch')
class PressUpdateView(View):

    def get(self, request, press_id):
        press = get_object_or_404(Press, pk=press_id)
        press_form = PressForm(instance=press)
        context = {
            'title': 'Edit Press',
            'press_form': press_form,
        }
        return render(request, 'book/press_page/create.html', context)

    def post(self, request, press_id):
        press = get_object_or_404(Press, pk=press_id)
        press_form = PressForm(request.POST or None, request.FILES or None, instance=press)
        if press_form.is_valid():
            instance = press_form.save(commit=False)
            instance.save()
            press_form.save_m2m()
            return HttpResponseRedirect(instance.get_absolute_url())
        context = {
            'title': 'Edit Press',
            'press_form': press_form,
        }
        return render(request, 'book/press_page/create.html', context)


@method_decorator(login_required, name='dispatch')
class PressDeleteView(View):

    def get(self, request, press_id):
        press = get_object_or_404(Press, pk=press_id)
        context = {
            'author': press,
        }
        return render(request, 'book/press_page/delete.html', context)

    def post(self, request, press_id):
        press = get_object_or_404(Press, pk=press_id)
        press.delete()
        return HttpResponseRedirect(reverse("book:press_index"))

