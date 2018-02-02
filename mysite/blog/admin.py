from django.contrib import admin
from .models import Post
# Register your models here.
# Related link: https://docs.djangoproject.com/en/2.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.search_fields


# admin.site.register(Post)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    date_hierarchy = 'update_date_time'
    list_display = ['blog_title', 'blog_author', 'update_date_time']
    list_filter = ['create_date_time', 'update_date_time', 'blog_author']
    search_fields = ['blog_title', 'blog_content']


