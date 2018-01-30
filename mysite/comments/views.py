from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Comment
from .forms import CommentForm


def detail(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment_instance = comment_form.save(commit=False)
            comment_instance.comment_user = request.user
            comment_instance.content_type = comment.content_type
            comment_instance.content_object = comment.content_object
            comment_instance.object_id = comment.object_id
            parent_id = request.POST.get('parent_id')
            if parent_id is not None:
                comment_instance.parent_comment = Comment.objects.get(pk=int(parent_id))
            comment_form.save()
            comment_form.save_m2m()
            return HttpResponseRedirect(comment.get_absolute_url())
    context = {
        'comment': comment,
        'comment_form': CommentForm(),
    }
    return render(request, 'comments/detail.html', context)


def delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == "POST":
        if comment.parent_comment:
            redirect_url = comment.parent_comment.get_absolute_url()
        else:
            redirect_url = comment.content_object.get_absolute_url()
        comment.delete()
        return HttpResponseRedirect(redirect_url)
    context = {
        'comment': comment,
    }
    return render(request, 'comments/delete.html', context)
