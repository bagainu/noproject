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
from .forms import BookShareListForm
from comments.forms import CommentForm
from comments.models import Comment

from utils.paginator import page_list
# Create your views here.


class ShareListIndexView(View):

    def get(self, request):
        book_sharelist = BookShareList.objects.order_by('-share_update_date_time')

        qs = request.GET.get('qs')
        if qs:
            book_sharelist = book_sharelist.filter(
                Q(share_title__icontains=qs) |
                Q(share_intro__icontains=qs) |
                Q(share_tag__name__icontains=qs)
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
                Q(share_intro__icontains=qs) |
                Q(share_tag__name__icontains=qs)
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
        share_form = BookShareListForm()
        context = {
            'title': 'New Share',
            'share_form': share_form,
            'previous_url': request.META.get('HTTP_REFERER'),
        }
        return render(request, 'sharelist/create.html', context)
    
    def post(self, request):
        share_form = BookShareListForm(request.POST or None, request.FILES or None)
        if share_form.is_valid():
            instance = share_form.save(commit=False)
            instance.save()
            share_form.save_m2m()
            return HttpResponseRedirect(instance.get_absolute_url())
        return self.get(request)


class ShareListDetailView(View):

    def get(self, request, share_id):
        bookshare = get_object_or_404(BookShareList, pk=share_id)
        bookshare_books = bookshare.share_books.all()
        page_bookshare_books = page_list(request, bookshare_books, 20)

        context = {
            'bookshare': bookshare,
            'bookshare_books': page_bookshare_books,
            'bookshare_comments': bookshare.share_comment.filter(parent_comment=None).order_by('-comment_date_time'),
            'comment_form': CommentForm(),
        }
        return render(request, 'sharelist/detail.html', context)
    
    def post(self, request, share_id):
        bookshare = get_object_or_404(BookShareList, pk=share_id)
        comment_form = CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment_instance = comment_form.save(commit=False)
            comment_instance.comment_user = request.user
            comment_instance.content_type = ContentType.objects.get_for_model(BookShareList)
            comment_instance.content_object =bookshare 
            comment_instance.object_id = bookshare.id
            parent_id = request.POST.get('parent_id')
            if parent_id is not None:
                comment_instance.parent_comment = Comment.objects.get(pk=int(parent_id))
            comment_form.save()
            comment_form.save_m2m()
            return HttpResponseRedirect(bookshare.get_absolute_url())
        return self.get(request, share_id)


@method_decorator(login_required, name='dispatch')
class ShareListUpdateView(View):

    def get(self, request, share_id):
        bookshare = get_object_or_404(BookShareList, pk=share_id)
        share_form = BookShareListForm(instance=bookshare)
        context = {
            'title': 'New Share',
            'share_form': share_form,
            'previous_url': request.META.get('HTTP_REFERER'),
        }
        return render(request, 'sharelist/create.html', context)
    
    def post(self, request, share_id):
        bookshare = get_object_or_404(BookShareList, pk=share_id)
        share_form = BookShareListForm(request.POST or None, request.FILES or None, instance=bookshare)
        if share_form.is_valid():
            instance = share_form.save(commit=False)
            instance.save()
            share_form.save_m2m()
            return HttpResponseRedirect(instance.get_absolute_url())
        return self.get(request, share_id)


@method_decorator(login_required, name='dispatch')
class ShareListDeleteView(View):

    def get(self, request, share_id):
        bookshare = get_object_or_404(BookShareList, pk=share_id)
        context = {
            'bookshare': bookshare,
        }
        return render(request, 'sharelist/delete.html', context)
    
    def post(self, request, share_id):
        bookshare = get_object_or_404(BookShareList, pk=share_id)
        bookshare.delete()
        return HttpResponseRedirect(reverse("sharelist:share_index_own", kwargs={ 'user_id': request.user.id }))
