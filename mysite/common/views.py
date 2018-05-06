from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.html import format_html
from django.views import View

from blog.models import Post
from book.models import Book
from sharelist.models import BookShareList, BookLog
from comments.models import Comment

from utils.paginator import page_list

# Create your views here.

class IndexView(View):

    def get(self, request):
        book_posts = Post.objects \
        .annotate(num_votes=Count('votes__user_id')) \
        .order_by('num_votes') \
        .order_by('-create_date_time')[:10]

        # the value of content_type__model must be in lowercase
        book_comments = Comment.objects \
        .filter(content_type__model='booklog', parent_comment=None) \
        .annotate(num_votes=Count('votes__user_id')) \
        .order_by('num_votes') \
        .order_by('-comment_date_time')[:10] 

        book_sharelist = BookShareList.objects \
        .annotate(num_votes=Count('votes__user_id')) \
        .order_by('num_votes') \
        .order_by('-share_create_date_time')[:10]

        context = {
            'book_posts': book_posts,
            'book_comments': book_comments,
            'book_sharelist': book_sharelist,
        }
        return render(request, 'common/index.html', context)
