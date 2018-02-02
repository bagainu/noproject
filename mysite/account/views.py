from django.shortcuts import render

from .forms import CustomUserRegisterForm, CustomUserLoginForm

# Create your views here.

def register(request):
    register_form = CustomUserRegisterForm(request.POST or None)
    if register_form.is_valid():
        register_form.save()
        return render("registered")

    context = {
        'user_form': register_form,
    }
    return render(request, 'account/register.html', context )


def login(request):
    pass


def logout(request):
    pass