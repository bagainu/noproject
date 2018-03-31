from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.html import format_html
from django.views import View

from .models import BookShareList, ShareTag

from utils.paginator import page_list
# Create your views here.


class ShareListIndexView(View):

    def get(self, request):
        book_sharelist = BookShareList.objects.order_by('-share_update_date_time')

        qs = request.GET.get('qs')
        if qs:
            book_sharelist = book_sharelist.filter(
                Q(share_title__icontains=qs) |
                Q(share_intro__icontains=qs)
            ).distinct()

        page_book_sharelist = page_list(request, book_sharelist, 20)
        tag_list = ShareTag.objects.all()

        context = {
            'title': 'Share Lists',
            'book_sharelist': page_book_sharelist,
            'tag_list': tag_list,
        }
        return render(request, 'sharelist/index.html', context)


class ShareListIndexOwnView(View):

    def get(self, request, user_id):
        user = get_object_or_404(get_user_model(), pk=user_id)
        book_sharelist = BookShareList.objects.filter(share_user=user).order_by('-share_update_date_time')

        qs = request.GET.get('qs')
        if qs:
            book_sharelist = book_sharelist.filter(
                Q(share_title__icontains=qs) |
                Q(share_intro__icontains=qs)
            ).distinct()

        page_book_sharelist = page_list(request, book_sharelist, 20)
        tag_list = ShareTag.objects.all()

        title = format_html("""<i>{0}</i>'s Share Lists""".format(user.username))
        if request.user == user:
            title = 'My Share Lists'

        context = {
            'title': title,
            'book_sharelist': page_book_sharelist,
            'tag_list': tag_list,
        }
        return render(request, 'sharelist/index.html', context)


@method_decorator(login_required, name='dispatch')
class ShareListCreateView(View):

    def get(self, request):
        return HttpResponse('create get')
    
    def post(self, request):
        return HttpResponse('create post')


class ShareListDetailView(View):

    def get(self, request, share_id):
        return HttpResponse('detail get')
    
    def post(self, request, share_id):
        return HttpResponse('detail post')


@method_decorator(login_required, name='dispatch')
class ShareListUpdateView(View):

    def get(self, request, share_id):
        return HttpResponse('update get')
    
    def post(self, request, share_id):
        return HttpResponse('update post')


@method_decorator(login_required, name='dispatch')
class ShareListDeleteView(View):

    def get(self, request, share_id):
        return HttpResponse('delete get')
    
    def post(self, request, share_id):
        return HttpResponse('delete post')
