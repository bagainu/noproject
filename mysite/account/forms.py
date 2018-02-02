from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import CustomUser


class CustomUserRegisterForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)   
    password_confirm = forms.CharField(label="Password Confirmation", widget=forms.PasswordInput)   

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
            raise forms.ValidationError('Password not match')
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
    pass


