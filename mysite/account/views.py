from django.contrib.auth import (
    authenticate as auth_authenticate,
    login as auth_login,
    logout as auth_logout,
)
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
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
        return HttpResponseRedirect(reverse("blog:blog_index"))
    context = {
        'user_form': register_form,
    }
    return render(request, 'account/register.html', context) 


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
    return render(request, 'account/login.html', context)


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
        print(request.POST)
        profile_form.save(commit=True)
        print(custom_user.avatar)
        return HttpResponseRedirect(reverse("blog:blog_index"))
    context = {
        'user_form': profile_form,
    }
    return render(request, 'account/profile.html', context)

