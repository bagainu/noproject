from django.contrib import admin  # NOQA

from .models import Vote
# Register your models here.


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    ordering = ['user_id', ]
    list_display = ['user_id', 'content_type', 'content_object', 'action', 'create_at', ]
    search_fields = ['user_id', 'content_type', 'action', ]

