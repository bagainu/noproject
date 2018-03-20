from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import F
from django.db.models.signals import pre_init, post_init
from django.dispatch import receiver

from star_ratings.models import UserRating

from book.models import Book
from blog.models import Post
from comments.models import Comment
# Create your models here.


class BookPost(models.Model):
    post_obj = models.OneToOneField(Post, on_delete=models.CASCADE, primary_key=True)
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey('content_type', 'object_id')


class BookRates(models.Model):
    post_obj = models.OneToOneField(UserRating, on_delete=models.CASCADE, primary_key=True)
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey('content_type', 'object_id')


class BookLog(models.Model):
    booklog_owner = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    booklog_book = models.ForeignKey(Book, on_delete=models.CASCADE, default=1)
    booklog_intro = models.TextField()
    booklog_rates = GenericRelation(BookRates, related_query_name='booklog_rates')
    booklog_comment = GenericRelation(Comment, related_query_name='booklog_comment')
    booklog_post = GenericRelation(BookPost, related_query_name='booklog_post')
    booklog_create_date_time = models.DateTimeField(auto_now=False, auto_now_add=True, help_text='data published')
    booklog_update_date_time = models.DateTimeField(auto_now=True, auto_now_add=False, help_text='data updated')

    def __str__(self):
        return "{0}'s book log of {1}".format(self.booklog_owner, self.booklog_book)

    def __unicode__(self):
        return "{0}'s book log of {1}".format(self.booklog_owner, self.booklog_book)


class BookShelf(models.Model):
    shelf_owner = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    shelf_name = models.CharField(max_length=200)
    shelf_books = models.ManyToManyField(Book)
    shelf_update_date_time = models.DateTimeField(auto_now=True, auto_now_add=False, help_text='data updated')

    def __str__(self):
        return "{0}'s bookshelf {1}".format(self.shelf_owner, self.shelf_name)

    def __unicode__(self):
        return "{0}'s bookshelf {1}".format(self.shelf_owner, self.shelf_name)

    
@receiver(pre_init, sender=Post)
def booklog_pre_init_callback(sender, instance, *args, **kwargs):
    pass
