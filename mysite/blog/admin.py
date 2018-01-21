from django.contrib import admin
from .models import Post, Author
# Register your models here.
# Related link: https://docs.djangoproject.com/en/2.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.search_fields


# admin.site.register(Post)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_time'
    list_display = ['blog_title', 'blog_author', 'date_time']
    list_filter = ['date_time', 'blog_author']
    search_fields = ['blog_title', 'blog_content']


#admin.site.register(Author)
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'reg_time']
    list_filter = ['reg_time']
    search_fields = ['email', 'first_name', 'last_name']

