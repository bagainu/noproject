from django.contrib import admin

from .models import BookShareList, ShareTag
# Register your models here.


@admin.register(BookShareList)
class BookShareListAdmin(admin.ModelAdmin):
    ordering = ['share_user', ]
    list_display = ['share_user', 'share_title', 'share_create_date_time', 'share_update_date_time', ]
    search_fields = ['share_user', 'share_title', ]


@admin.register(ShareTag)
class ShareTagAdmin(admin.ModelAdmin):
    pass