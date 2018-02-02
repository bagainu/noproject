from django.contrib.auth import (
    authenticate as auth_authenticate,
    login as auth_login,
    logout as auth_logout,
)
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import CustomUserRegisterForm, CustomUserLoginForm

# Create your views here.


def _get_next_url(request):
    next_url = None
    try:
        next_url = request.GET.get('next')
    except:
        pass
    try:
        next_url = request.POST.get('next')
    except:
        pass
    return next_url


def register(request):
    next_url = _get_next_url(request)
    register_form = CustomUserRegisterForm(request.POST or None)
    if register_form.is_valid():
        user = register_form.save()
        auth_login(request, user)
        if next_url is not None:
            return HttpResponseRedirect(next_url)
        return HttpResponseRedirect(reverse("blog:blog_index"))
    context = {
        'user_form': register_form,
    }
    return render(request, 'account/register.html', context) 


def login(request):
    next_url = _get_next_url(request)
    login_form = CustomUserLoginForm(request.POST or None)
    if login_form.is_valid():
        user = login_form.save()
        auth_login(request, user)
        if next_url is not None:
            return HttpResponseRedirect(next_url)
        return HttpResponseRedirect(reverse("blog:blog_index"))
    context = {
        'user_form': login_form,
    }
    return render(request, 'account/login.html', context)


def logout(request):
    next_url = _get_next_url(request)
    auth_logout(request)
    if next_url:
        return HttpResponseRedirect(next_url)
    return HttpResponseRedirect(reverse("blog:blog_index"))

