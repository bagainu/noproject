from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import (
    AdminPasswordChangeForm,
    UserChangeForm, 
    UserCreationForm,
)
from .models import CustomUser
from .forms import (
    CustomUserRegisterForm, 
    CustomUserUpdateForm,
    CustomUserLoginForm,
)
# Register your models here.

# Currently not using built-in permissions, so unregister Group model
admin.site.unregister(Group)

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    readonly_fields = ('register_time',)

    form = CustomUserUpdateForm
    add_form = CustomUserRegisterForm
    change_password_form = AdminPasswordChangeForm

    fieldsets = (
        (None, {'fields': ('email', 'password', 'register_time', )}),
        ('Personal info', {'fields': ('username', 'avatar', 'gender', 'intro', 'following', 'followed')}),
        ('Permissions', {'fields': ('is_admin', 'is_active', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password', 'password_confirm', 'gender', 'intro')}
        ),
    )
    list_display = ('email', 'username', 'gender', 'is_admin', 'is_active')
    list_filter = ('is_admin', 'is_active')
    search_fields = ('email', 'username', 'is_admin', 'is_active')
    ordering = ('email',)
    filter_horizontal = ()
