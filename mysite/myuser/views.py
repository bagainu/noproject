from django.contrib.auth import (
    authenticate as auth_authenticate,
    login as auth_login,
    logout as auth_logout,
)
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import CustomUser
from .forms import (
    CustomUserRegisterForm, 
    CustomUserLoginForm,
    CustomUserProfileForm,
)

# Create your views here.


def _get_next_url(request):
    next_url = None
    if hasattr(request, 'GET'):
        next_url = request.GET.get('next')
    elif hasattr(request, 'POST'):
        next_url = request.POST.get('next')
    return next_url


def register(request):
    next_url = _get_next_url(request)
    register_form = CustomUserRegisterForm(request.POST or None)
    if register_form.is_valid():
        user = register_form.save()
        auth_login(request, user)
        if next_url is not None:
            return HttpResponseRedirect(next_url)
        return HttpResponseRedirect(reverse("myuser:user_profile", kwargs={ 'user_id': user.id }))
    context = {
        'user_form': register_form,
    }
    return render(request, 'myuser/register.html', context) 


def login(request):
    next_url = _get_next_url(request)
    login_form = CustomUserLoginForm(request.POST or None)
    if login_form.is_valid():
        auth_login(request, login_form.get_user())
        if next_url is not None:
            return HttpResponseRedirect(next_url)
        return HttpResponseRedirect(reverse("blog:blog_index"))
    context = {
        'user_form': login_form,
    }
    return render(request, 'myuser/login.html', context)


def logout(request):
    next_url = _get_next_url(request)
    auth_logout(request)
    if next_url:
        return HttpResponseRedirect(next_url)
    return HttpResponseRedirect(reverse("blog:blog_index"))


def profile(request, user_id):
    custom_user = get_object_or_404(CustomUser, id=user_id)
    profile_form = CustomUserProfileForm(request.POST or None, request.FILES or None, instance=custom_user)
    if profile_form.is_valid():
        instance = profile_form.save(commit=True)
        return redirect(instance, permanent=True)
    context = {
        'custom_user': custom_user,
        'user_form': profile_form,
    }
    return render(request, 'myuser/profile.html', context)


@login_required
def ajax_follow(request, user_id):
    if not request.is_ajax():
        raise Http404('Not an ajax call')
    if request.method == 'POST':
        target_user_id = request.GET.get('user')
        if target_user_id and target_user_id != request.user.id:
            target_user = get_object_or_404(CustomUser, id=target_user_id)
            custom_user = get_object_or_404(CustomUser, id=user_id)
            custom_user.following.add(target_user)
            target_user.followed.add(custom_user)
            return JsonResponse({ "return_id": target_user_id })
    return JsonResponse({ "return_id": -1 })
    

@login_required
def ajax_unfollow(request, user_id):
    if not request.is_ajax():
        raise Http404('Not an ajax call')
    if request.method == 'POST':
        target_user_id = request.GET.get('user')
        if target_user_id and target_user_id != request.user.id:
            target_user = get_object_or_404(CustomUser, id=target_user_id)
            custom_user = get_object_or_404(CustomUser, id=user_id)
            custom_user.following.remove(target_user)
            target_user.followed.remove(custom_user)
            return JsonResponse({ "return_id": target_user_id })
    return JsonResponse({ "return_id": -1 })



