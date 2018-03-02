from django.contrib import admin

from .models import BookLog, BookShelf
# Register your models here.

@admin.register(BookLog)
class BookLogAdmin(admin.ModelAdmin):
    ordering = ['booklog_owner', ]
    list_display = ['booklog_owner', 'booklog_book', 'booklog_update_date_time', 'booklog_create_date_time', ]
    search_fields = ['booklog_owner', 'booklog_book', ]


@admin.register(BookShelf)
class BookShelfAdmin(admin.ModelAdmin):
    ordering = ['shelf_owner', ]
    list_display = ['shelf_owner', 'shelf_name', 'shelf_update_date_time', ]
    search_fields = ['shelf_owner', 'shelf_name', ]