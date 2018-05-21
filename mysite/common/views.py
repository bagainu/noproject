from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.html import format_html
from django.views import View

from blog.models import Post
from book.models import Book
from sharelist.models import BookShareList, BookLog
from comments.models import Comment

from utils.paginator import page_list

TAB_POSTS = 0
TAB_NOTES = 1
TAB_SHARES = 2

# Create your views here.

def get_post_list():
    obj_list = Post.objects \
    .annotate(num_votes=Count('votes__user_id')) \
    .order_by('num_votes') \
    .order_by('-create_date_time')[:10],
    context = {
        'post_list': obj_list,
    }
    return render_to_string('blog/posts.html', context)


def get_notes_list():
    obj_list = Comment.objects \
    .filter(content_type__model='booklog', parent_comment=None) \
    .annotate(num_votes=Count('votes__user_id')) \
    .order_by('num_votes') \
    .order_by('-comment_date_time')[:10],
    context = {
        'comment_list': obj_list,
        'card_mode': True,
        'disable_delete': True,
        'disable_reply': False,
    }
    return render_to_string('comments/comments.html', context)


def get_share_list():
    obj_list = BookShareList.objects \
    .annotate(num_votes=Count('votes__user_id')) \
    .order_by('num_votes') \
    .order_by('-share_create_date_time')[:10]
    context = {
        'book_sharelist': obj_list,
        'slice_range': ":7",
    }
    return render_to_string('sharelist/sharelist.html', context)


def get_tab_list_html(tab_id):

    tab_list = {
        TAB_POSTS: Post.objects \
        .annotate(num_votes=Count('votes__user_id')) \
        .order_by('num_votes') \
        .order_by('-create_date_time')[:10],

        TAB_NOTES: Comment.objects \
        .filter(content_type__model='booklog', parent_comment=None) \
        .annotate(num_votes=Count('votes__user_id')) \
        .order_by('num_votes') \
        .order_by('-comment_date_time')[:10],

        TAB_SHARES: BookShareList.objects \
        .annotate(num_votes=Count('votes__user_id')) \
        .order_by('num_votes') \
        .order_by('-share_create_date_time')[:10]
    }


class IndexView(View):

    def get(self, request):
        context = {
            # 'book_posts': get_tab_list(TAB_POSTS),
            # 'book_comments': get_tab_list(TAB_NOTES),
            # 'book_sharelist': get_tab_list(TAB_SHARES),
            'book_posts_html': get_post_list(),
            'book_comments_html': get_notes_list(),
            'book_sharelist_html': get_share_list(),
        }
        return render(request, 'common/index.html', context)


def ajax_tab_list(request, tab_id):
    if not request.is_ajax():
        raise Http404('Not an ajax call')
    tab_list = get_tab_list(tab_id)
    if request.method == 'POST':
        return JsonResponse({'tab_list': tab_list })
    return JsonResponse({'tab_list': [] })
