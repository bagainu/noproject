from django.contrib import admin

from .models import (
    Author,
    Press,
    Book,
    BookTag,
)
# Register your models here.

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    ordering = ['author_name', ]
    list_display = ['author_name', ]
    search_fields = ['author_name', ]
    

@admin.register(Press)
class PressAdmin(admin.ModelAdmin):
    ordering = ['press_name', ]
    list_display = ['press_name', ]
    search_fields = ['press_name', ]


# admin.site.register(Post)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    ordering = ['book_title', ]
    list_display = ['book_title', 'authors', 'presses']
    search_fields = ['book_title', 'authors', 'presses']


@admin.register(BookTag)
class BookTagAdmin(admin.ModelAdmin):
    pass
