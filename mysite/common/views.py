from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.html import format_html
from django.views import View

from blog.models import Post
from sharelist.models import BookShareList, BookLog
from comments.models import Comment

from utils.paginator import page_list

# Create your views here.

class IndexView(View):

    def get(self, request):
        return render(request, 'common/index.html')
