from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from utils.image_utils import image_upload_to
from utils.string_utils import is_email_format
from .models import CustomUser


class CustomUserRegisterForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)   
    password_confirm = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)   

    class Meta:
        model = CustomUser
        fields = [
            'email',
            'username',
            'password',
            'password_confirm'
        ]

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Passwords not match')
        return password
    
    def save(self, commit=True):
        user = super().save(False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user


class CustomUserUpdateForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = [
            'email',
            'username',
            'password',
            'is_admin',
            'is_active',
        ]
    
    def clean_password(self):
        return self.initial.get('password')


class CustomUserLoginForm(forms.ModelForm):
    username = forms.CharField(label='Username or Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)   

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'password',
        ]

    def clean(self, *args, **kwargs):
        username_or_email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username_or_email and password:
            try:
                if is_email_format(username_or_email):
                    query_user = CustomUser.objects.get(email=username_or_email)
                else:
                    query_user = CustomUser.objects.get(username=username_or_email)
            except:
                raise forms.ValidationError('User not exists')
            user = authenticate(email=query_user.email, password=password)
            if not user:
                raise forms.ValidationError('Password incurrect')
            if not user.is_active:
                raise forms.ValidationError('User no longer valid. Please contact admin')
        # return super().clean(*args, **kwargs)

    def get_user(self):
        username_or_email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if is_email_format(username_or_email):
            user = authenticate(email=username_or_email, password=password)
        else:
            user = authenticate(email=CustomUser.objects.get(username=username_or_email).email, password=password)
        return user


class CustomUserProfileForm(forms.ModelForm):
    email = forms.EmailField(disabled=True)

    class Meta:
        model = CustomUser
        fields = [
            'email',
            'username',
            'avatar',
        ]
